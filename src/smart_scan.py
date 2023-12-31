import logging
import sys
import yaml
import os
from utils import github, open_ai


def get_config(config_file):
    with open(config_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            raise Exception("Invalid config file. Initiating a scan.")


# Sets the output of the action to the given value
def set_action_output(value):
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("{0}={1}\n".format("decision", value))


def main():
    logging.info("Starting smart scan action")

    logging.info("Retrieving config")
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.yml")
        config = get_config(config_path)
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    logging.info("Retrieving event context")
    gh_ctx = github.EventContext()

    logging.info("Validating inputs")
    try:
        gh_ctx.validate_inputs()
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    # This forces the action to run ONLY on PR.
    logging.info("Checking if this is a pull request")
    if not gh_ctx.action:
        logging.info("Trigger is not a PR. Initiating a scan.")
        set_action_output("yes")
        sys.exit()

    logging.info("Retrieving diff from GitHub")
    gh_client = github.API(gh_ctx.vars["gh_token"])
    try:
        diff = gh_client.get_diff(gh_ctx.url)
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    # Check the length of the diff. If it's too long, exit
    if len(diff) > 40000:
        logging.info("Diff is too large. Initiating a scan.")
        set_action_output("yes")
        sys.exit()

    # Establish the client for the appropriate API
    try:
        if gh_ctx.vars["openai_api_key"]:
            logging.info("Establishing OpenAI client")
            openai_client = open_ai.OpenAIClient(
                gh_ctx.vars["openai_api_key"],
                gh_ctx.vars["model"],
                config["prompt"],
                config["temperature"],
                )
        elif gh_ctx.vars["azure_api_key"]:
            logging.info("Establishing Azure client")
            openai_client = open_ai.AzureClient(
                gh_ctx.vars["azure_api_key"],
                gh_ctx.vars["model"],
                config["prompt"],
                config["temperature"],
                gh_ctx.vars["azure_endpoint"],
                gh_ctx.vars["azure_deployment_id"],
            )
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    logging.info("Generating decision from the model")
    try:
        decision = openai_client.get_decision(diff)
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    logging.info(f"Response decision: {decision['decision']}")
    logging.info(f"Response reason: {decision['reason']}")

    # If the decision is "no", add a comment to the pull request
    if decision["decision"] == "no":
        logging.info("Adding comment to pull request")
        try:
            gh_client.add_comment(
                gh_ctx.comment_url,
                config['comment'] + decision["reason"]
            )
        except Exception as e:
            logging.error(e)
            set_action_output("yes")
            sys.exit(1)

    set_action_output(decision["decision"])


if __name__ == "__main__":
    main()
