import openai

# This class is responsible for the OpenAI API
class OpenAI:
    def __init__(self, inputs):
        self.api_key = inputs['openai_api_key'] or inputs['azure_api_key']
        self.api_url = "https://api.openai.com/v1/engines/davinci/completions"