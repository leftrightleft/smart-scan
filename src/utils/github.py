import requests
import logging
import os
import json

class EventContext:
    # setting the context from the GitHub event
    def __init__(self):
        self._get_action_context()
        self.vars = self._get_env_vars()
        # TODO logging here
        logging.info("Successfully set context")

    def _get_env_vars(self):
        # returns a dictionary of input variables set by the action
        input_vars = {}
        for var in os.environ:
            if var.startswith("INPUT_"):
                input_vars[var] = os.environ[var]
        return input_vars

    def _get_action_context(self):
        try:
            with open("/github/workflow/event.json", "r") as file:
                contents = file.read()
                data = json.loads(contents)
        except FileNotFoundError:
            raise Exception("Could not find event.json.  Are you running this locally?")

        # check if this is a pull request
        action = data.get("action")
        if action in ["synchronize", "opened"]:
            self["action"] = action
            self["diff_url"] = data["pull_request"]["diff_url"]
            self["comment_url"] = data["pull_request"]["comments_url"]
        elif "compare" in data:
            self["action"] = "commit"
            self["diff_url"] = data["compare"] + ".diff"

    
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
        
