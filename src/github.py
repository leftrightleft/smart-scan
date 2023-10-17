import requests
import logging
import os

class GitHubAPI:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }

    def get_diff(self, compare_url):
        response = requests.get(compare_url, headers=self.headers)
        if response.status_code == 200:
            logging.info("Successfully retrieved diff")
            return response.text
        else:
            e = f"Error retrieving diff.  Response: {response.json()}"
            logging.error(e)
            raise Exception(e)
        
    def add_comment(self, comment_url, comment):
        data = {"body": comment}
        response = requests.post(comment_url, headers=self.headers, json=data)
        if response.status_code == 201:
            logging.info("Successfully added comment")
        else:
            e = f"Error adding comment. Response: {response.json()}"
            logging.error(e)
            raise Exception(e)
        
class Context:
    # setting the context from the GitHub event
    def _get_env_vars(self):
        # returns a dictionary of input variables set by the action
        input_vars = {}
        for var in os.environ:
            if var.startswith("INPUT_"):
                input_vars[var] = os.environ[var]
        return input_vars
    

    def _get_context(self):
        # returns the execution context of this run. Checks to see if this is a PR or a commit
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