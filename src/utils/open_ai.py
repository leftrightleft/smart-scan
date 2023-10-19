import openai
import json


class OpenAIClient:
    """
    A client for the OpenAI API.

    Attributes:
        api_key (str): The API key for the OpenAI API.
        model (str): The name of the GPT-3 model to use for generating text.
        system_prompt (str): The prompt to use for the system message.
        temperature (float): The temperature to use for generating text.
    """
    def __init__(self, api_key, model, system_prompt, temperature):
        openai.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature

    def get_decision(self, diff):
        """
        Calls the OpenAI API to generate a decision based on a diff.

        Args:
            diff (str): The diff to use for generating the decision.

        Returns:
            dict: A dictionary containing the decision and reason.
        """
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": diff},
                ],
                temperature=self.temperature
            )
            response = json.loads(completion.choices[0].message["content"])

            decision = {
                "decision": response["decision"].lower(),
                "reason": response["reason"].strip(),
            }
            return decision
        except Exception as e:
            raise Exception(f"Error generating decision: {e}")


class AzureClient:
    """
    A client for the Azure API.

    Attributes:
        api_key (str): The API key for the Azure API.
        model (str): The name of the GPT-3 model to use for generating text.
        system_prompt (str): The prompt to use for the system message.
        temperature (float): The temperature to use for generating text.
        endpoint (str): The endpoint URL for the Azure API.
        deployment_id (str): The deployment ID for the Azure API.
    """
    def __init__(self, api_key, model, system_prompt, temperature, endpoint, deployment_id):
        openai.api_key = api_key
        openai.api_base = endpoint
        openai.api_type = "azure"
        openai.api_version = "2023-05-15"   
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.deployment_id = deployment_id

    def get_decision(self, diff):
        """
        Calls the Azure API to generate a decision based on a diff.

        Args:
            diff (str): The diff to use for generating the decision.

        Returns:
            dict: A dictionary containing the decision and reason.
        """
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": diff},
            ],
            temperature=self.temperature,
            deployment_id=self.deployment_id,
        )
        response = json.loads(completion.choices[0].message["content"])

        decision = {
            "decision": response["decision"].lower(),
            "reason": response["reason"].strip(),
        }
        return decision
