import openai
import json

temperature = 0.1
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()


class OpenAIClient:
    """
    A client for the OpenAI API.

    This class provides a simple interface for calling the OpenAI API to generate text based on a given prompt.
    The client takes an API key and a GPT-3 model as input, and provides a `get_decision` method for generating
    text based on a given diff.

    Attributes:
        api_key (str): The API key for the OpenAI API.
        model (str): The name of the GPT-3 model to use for generating text.
    """
    def __init__(self, api_key, model):
        openai.api_key = api_key
        self.model = model
    
    def get_decision(self, diff):
        """
        Calls the OpenAI API to generate a decision based on a diff.

        This method takes a diff as input and calls the OpenAI API to generate a decision based on the diff.
        The decision is returned as a dictionary with two keys: "decision" and "reason". The "decision" key
        contains the lowercase version of the decision text returned by the API, and the "reason" key contains
        the original decision text returned by the API.

        Args:
            diff (str): The diff to use for generating the decision.

        Returns:
            dict: A dictionary containing the decision and reason.
        """
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff},
            ],
            temperature = temperature
        )
        response = json.loads(completion.choices[0].message["content"])

        decision = {
            "decision": response["decision"].lower(),
            "reason": response["reason"].strip(),
        }
        return decision
    

class AzureClient:
    """
    A client for the Azure API.

    This class provides a simple interface for calling the Azure API to generate text based on a given prompt.
    The client takes an API key, a GPT-3 model, an endpoint URL, and a deployment ID as input, and provides a
    `get_decision` method for generating text based on a given diff.

    Attributes:
        api_key (str): The API key for the Azure API.
        model (str): The name of the GPT-3 model to use for generating text.
        endpoint (str): The endpoint URL for the Azure API.
        deployment_id (str): The deployment ID for the Azure API.
    """
    def __init__(self, api_key, model, endpoint, deployment_id):
        self.api_key = api_key
        self.model = model
        self.deployment_id = deployment_id
        openai.api_type = "azure"
        openai.api_base = endpoint
        openai.api_version = "2023-05-15"   

    def get_decision(self, diff):
        """
        Calls the Azure API to generate a decision based on a diff.

        This method takes a diff as input and calls the Azure API to generate a decision based on the diff.
        The decision is returned as a dictionary with two keys: "decision" and "reason". The "decision" key
        contains the lowercase version of the decision text returned by the API, and the "reason" key contains
        the original decision text returned by the API.

        Args:
            diff (str): The diff to use for generating the decision.

        Returns:
            dict: A dictionary containing the decision and reason.
        """
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff},
            ],
            temperature = temperature,
            deployment_id=self.deployment_id,
        )
        response = json.loads(completion.choices[0].message["content"])

        decision = {
            "decision": response["decision"].lower(),
            "reason": response["reason"].strip(),
        }
        return decision

