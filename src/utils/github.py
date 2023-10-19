import requests
import logging
import os
import json

class EventContext:
    """
    Provides context information for a GitHub event.

    This class retrieves information about the event from the event.json file inside the actions container and sets the context
    for the event. The context includes the action that triggered the event (e.g. "synchronize" or "opened"),
    as well as the URLs for the diff and comments associated with the event.

    Attributes:
        vars (dict): A dictionary of input variables set by the action. These are the action inputs that
            are used to configure the OpenAI or Azure client.
    """
    def __init__(self):
        self.__get_action_context()
        self.vars = self.__get_env_vars()

    def __get_action_context(self):
        """
        Retrieves context information for the GitHub event.

        This method reads the contents of the event.json file to retrieve information about the event.
        If the event is a pull request or a commit, the method sets the action to "synchronize" or "commit",
        respectively, and sets the URLs for the diff and comments associated with the event.

        Raises:
            Exception: If the event.json file cannot be found.

        Returns:
            None
        """
        try:
            with open("/github/workflow/event.json", "r") as file:
                contents = file.read()
                data = json.loads(contents)
        except FileNotFoundError:
            raise Exception("Could not find event.json.  Are you running this locally?")

        # check if this is a pull request or commit
        action = data.get("action")
        if action in ["synchronize", "opened"]:
            self.action = action
            self.diff_url = data["pull_request"]["diff_url"]
            self.comment_url = data["pull_request"]["comments_url"]
        elif "compare" in data:
            self.action = "commit"
            self.diff_url = data["compare"] + ".diff"

   
    def __get_env_vars(self):
        """
        Retrieves input variables set by the action.

        This method retrieves input variables set by the action from the environment variables
        passed to the workflow. The input variables are returned as a dictionary with the following keys:

        - "gh_token": The GitHub token used to authenticate API requests.
        - "model": The name of the GPT-3 model to use for generating text.
        - "openai_api_key": The API key for the OpenAI API.
        - "azure_api_key": The API key for the Azure API.
        - "azure_endpoint": The endpoint URL for the Azure API.
        - "azure_deployment_id": The deployment ID for the Azure API.

        If an input variable is not set, its value in the dictionary will be `None`.

        Returns:
            dict: A dictionary containing the input variables set by the action.
        """
        input_vars = {
            "gh_token": os.environ.get("INPUT_GH_TOKEN"),
            "model": os.environ.get("INPUT_MODEL"),
            "openai_api_key": os.environ.get("INPUT_OPENAI_API_KEY"),
            "azure_api_key": os.environ.get("INPUT_AZURE_API_KEY"),
            "azure_endpoint": os.environ.get("INPUT_AZURE_ENDPOINT"),
            "azure_deployment_id": os.environ.get("INPUT_AZURE_DEPLOYMENT_ID"),
        }
        
        # set empty strings to None
        input_vars = {
            key: value if value != "" else None
            for key, value in input_vars.items()
        }
        return input_vars

    def validate_inputs(self):
        """
        Validates the input variables set by the action.

        This method checks that the input variables set by the action are valid. Specifically, it checks that:

        - Either the OpenAI API key or the Azure API key is set (but not both).
        - If the Azure API key is set, the Azure endpoint and deployment ID are also set.

        Raises:
            Exception: If the input variables are not valid.

        Returns:
            None
        """
        openai_key = self.vars["openai_api_key"]
        azure_key = self.vars["azure_api_key"]
        azure_endpoint = self.vars["azure_endpoint"]
        azure_deployment_id = self.vars["azure_deployment_id"]

        if not openai_key and not azure_key:
            raise Exception("Both openai_api_key and azure_api_key are empty. Exiting.")

        if openai_key and azure_key:
            raise Exception("Both openai_api_key and azure_api_key are set. Exiting.")

        if azure_key and (not azure_endpoint or not azure_deployment_id):
            raise Exception("azure_api_key is set, but azure_endpoint or azure_deployment_id is not set. Exiting.")


class API:
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
        
