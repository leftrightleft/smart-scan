# import os
import logging
import github
import sys
import openai
import json
import yaml
import os


logging.basicConfig(filename="logging.log", level=logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

open_ai_key = sys.argv[1]
gh_token = sys.argv[2]


def get_config(config_file):
    with open(config_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logging.error(e)
            sys.exit(1)


def get_context():
    ctx = {}
    with open("/github/workflow/event.json", "r") as file:
        contents = file.read()
        data = json.loads(contents)

    # check if this is a pull request
    action = data.get("action")
    if action in ["synchronize", "opened"]:
        ctx["action"] = action
        ctx["diff_url"] = data["pull_request"]["diff_url"]
        ctx["comment_url"] = data["pull_request"]["comments_url"]
    elif "compare" in data:
        ctx["action"] = "commit"
        ctx["diff_url"] = data["compare"] + ".diff"

    return ctx


def set_action_output(output_name, value):
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a") as f:
            f.write("{0}={1}\n".format(output_name, value))
            print("::set-output name={0}::{1}".format(output_name, value), file=sys.stdout)


def main():
    gh = github.Client(gh_token)
    openai.api_key = open_ai_key
    config = get_config("/smart-scan/config.yml")
    ctx = get_context()
    print(ctx)
    diff = gh.get_diff(ctx["diff_url"])

    completion = openai.ChatCompletion.create(
        model=config["model"],
        messages=[
            {"role": "system", "content": config["prompt"]},
            {"role": "user", "content": diff},
        ],
    )
    response = json.loads(completion.choices[0].message["content"])

    logging.info(f"Response decision: {response['decision']}")
    logging.info(f"Response reason: {response['reason']}")

    if ctx["action"] in ["synchronize", "opened"]:
        comment = f"{config['comment']} \n\n**Decision:** {response['decision']} \n\n**Reason:** {response['reason']}"
        gh.add_comment(ctx["comment_url"], comment)

    set_action_output("decision", response["decision"])


if __name__ == "__main__":
    main()
