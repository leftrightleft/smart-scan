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
# compare_url = sys.argv[3]
# model_name = "gpt-3.5-turbo"
# prompt = """
# You are a decision tool which decides whether or not a static analysis should occur using CodeQL 
# on the following changed code.  You will decide yes for any changes that could introduce a security concern. 

# The code snippet provided will be a diff from a GitHub pull request. You will analyze the 
# diff and give a response of yes or no along with an explanation.  Yes indicates a static analysis should occur, 
# no indicates there are no changes that could be a security concern. 

# Your response should be formatted in json format.  "yes" or "no" will be in a key called "decision".  
# The reason for the decision will be in a key called "reason".  

# An example: {"decision" : "no", "reason" : "there are no changes that could introduce a security concern in this code diff. The changes made in this diff are related to importing and renaming some modules, modifying the module name, and updating the query to use the new module. These changes do not introduce any security vulnerabilities or risks."}
# """

logging.info("Starting smart-scan")
# logging.info(f"Diff URL: {compare_url}")

def get_config(config_file):
    with open(config_file, "r") as stream:
        try:
            return yaml.safe_load(stream)["bootcamp-setup"]
        except yaml.YAMLError as e:
            logging.error(e)
            sys.exit(1)

def parse_event():
    with open("/github/workflow/event.json", "r") as file:
        contents = file.read()
        print(contents)
    return json.loads(contents)

def main():
    print(os.getcwd())
    print(os.listdir("/"))
    print(os.listdir("/github"))

    gh = github.Client(gh_token)
    openai.api_key = open_ai_key
    config = get_config("/github/workspace/smart-scan/config.yml")
    event = parse_event()
    diff = gh.get_diff(event["compare"] + ".diff")
    completion = openai.ChatCompletion.create(
        model=config["model"],
        messages=[
            {"role": "system", "content": config["prompt"]},
            {"role": "user", "content": diff},
        ],
    )

    response = json.loads(completion.choices[0].message['content'])
    logging.info(f"Response content: {response['decision']}")
    logging.info(f"Response reason: {response['reason']}")


if __name__ == "__main__":
    main()
