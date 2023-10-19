# import os
import logging
import sys
import json
import yaml
import os
from utils import github, open_ai


def set_action_output(value):
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("{0}={1}\n".format("decision", value))


def main():
    gh_ctx = github.EventContext()

    # Validate inputs and trigger scan if invalid
    try:
        gh_ctx.validate_inputs()
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    # Check if this is a direct commit. If yes, trigger scan
    if gh_ctx.action == "commit":
        logging.info("Direct commit detected. Exiting.")
        set_action_output("yes")
        sys.exit()

    # Connect to GitHub and retrieve the diff
    gh_client = github.API(gh_ctx.vars["gh_token"])
    try:
        diff = gh_client.get_diff(gh_ctx.diff_url)
    except Exception as e:
        set_action_output("yes")
        sys.exit(1)

    # Establish OpenAI or Azure client 
    if gh_ctx.vars["openai_api_key"]:
        openai_client = open_ai.OpenAIClient(gh_ctx.vars["openai_api_key"])
    elif gh_ctx.vars["azure_api_key"]:
        openai_client = open_ai.AzureClient(
            gh_ctx.vars["azure_api_key"],
            gh_ctx.vars["azure_endpoint"],
            gh_ctx.vars["azure_deployment"],
        )

    # Get the decision
    try:
        decision = openai_client.get_decision(diff)
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    logging.info(f"Response decision: {decision['decision']}")
    logging.info(f"Response reason: {decision['reason']}")

    set_action_output(decision["decision"])


if __name__ == "__main__":
    main()
