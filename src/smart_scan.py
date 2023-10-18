# import os
import logging
import sys
import openai
import json
import yaml
import os

from utils import github, openai
# from .github.github import API, Context as gh_api, gh_context


# logging.basicConfig(filename="logging.log", level=logging.INFO)
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setLevel(logging.INFO)
# console_formatter = logging.Formatter("%(levelname)s: %(message)s")
# console_handler.setFormatter(console_formatter)
# logging.getLogger().addHandler(console_handler)


# # retrieve inputs from the workflow file
# def get_inputs():
#     inputs = {}
#     inputs["gh_token"] = sys.argv[1] if sys.argv[1] != "" else None
#     inputs["model"] = sys.argv[2] if sys.argv[2] != "" else None
#     inputs["openai_api_key"] = sys.argv[3] if sys.argv[3] != "" else None
#     inputs["azure_api_key"] = sys.argv[4] if sys.argv[4] != "" else None
#     inputs["azure_endpoint"] = sys.argv[5] if sys.argv[5] != "" else None
#     # inputs["azure_deployment"] = sys.argv[6] if sys.argv[6] != "" else None

#     # Check if both openai_api_key and azure_api_key are set
#     if inputs["openai_api_key"] and inputs["azure_api_key"]:
#         logging.error("Both openai_api_key and azure_api_key are set. Exiting.")
#         Actions.set_output("yes")
#         sys.exit(1)

#     # Check if both openai_api_key and azure_api_key are empty
#     if inputs["openai_api_key"] is None and inputs["azure_api_key"] is None:
#         logging.error("Both openai_api_key and azure_api_key are empty. Exiting.")
#         Actions.set_output("yes")
#         sys.exit(1)

#     return inputs

# def get_config(config_file):
#     with open(config_file, "r") as stream:
#         try:
#             return yaml.safe_load(stream)
#         except yaml.YAMLError as e:
#             logging.error(e)
#             Actions.set_output("yes")
#             sys.exit(1)

# def get_event_context():
#     ctx = EventContext()
#     with open("/github/workflow/event.json", "r") as file:
#         contents = file.read()
#         data = json.loads(contents)

#     # check if this is a pull request
#     action = data.get("action")
#     if action in ["synchronize", "opened"]:
#         ctx["action"] = action
#         ctx["diff_url"] = data["pull_request"]["diff_url"]
#         ctx["comment_url"] = data["pull_request"]["comments_url"]
#     elif "compare" in data:
#         ctx["action"] = "commit"
#         ctx["diff_url"] = data["compare"] + ".diff"

#     return ctx


def set_action_output(value):
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("{0}={1}\n".format("decision", value))


def main():
    gh_ctx = github.EventContext()

    # Validate inputs
    try:
        gh_ctx.validate_inputs()
    except Exception as e:
        logging.error(e)
        set_action_output("yes")
        sys.exit(1)

    if gh_ctx.action == "commit":
        sys.exit()

    # if gh_ctx.vars
    # print(gh_ctx.vars)
    # inputs = get_inputs()
    # config = get_config("/smart-scan/config.yml")

    # gh_api = GitHubAPI(inputs['gh_token'])

    # openai.api_key = inputs['openai_api_key'] or inputs['azure_api_key']
    # diff = gh.get_diff(ctx["diff_url"])

    # completion = openai.ChatCompletion.create(
    #     model=config["model"],
    #     messages=[
    #         {"role": "system", "content": config["prompt"]},
    #         {"role": "user", "content": diff},
    #     ],
    # )
    # response = json.loads(completion.choices[0].message["content"])

    # logging.info(f"Response decision: {response['decision']}")
    # logging.info(f"Response reason: {response['reason']}")

    # if ctx["action"] in ["synchronize", "opened"]:
    #     comment = f"{config['comment']} \n\n**Decision:** {response['decision']} \n\n**Reason:** {response['reason']}"
    #     gh.add_comment(ctx["comment_url"], comment)

    # set_action_output(response["decision"])


if __name__ == "__main__":
    main()
