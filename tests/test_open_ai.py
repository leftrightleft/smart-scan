import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import openai

from src.utils.open_ai import OpenAIClient, AzureClient

# Super hacky way to import modules from the src directory because I cant figure out how the f to use unit tests properly
sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src/utils")

class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        self.client = OpenAIClient("test_api_key", "test_model", "test_prompt", 0.0)

    def test_init(self):
        api_key = "test_api_key"
        model = "test_model"
        system_prompt = "test_system_prompt"
        temperature = 0.5

        client = OpenAIClient(api_key, model, system_prompt, temperature)

        self.assertEqual(openai.api_key, api_key)
        self.assertEqual(client.model, model)
        self.assertEqual(client.system_prompt, system_prompt)
        self.assertEqual(client.temperature, temperature)
    
    @patch("openai.ChatCompletion.create")
    def test_get_decision(self, mock_create):
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message={"content": '{"decision": "yes", "reason": "because."}'})]
        mock_create.return_value = mock_completion

        diff = "This is a test diff."
        expected_decision = {"decision": "yes", "reason": "because."}
        actual_decision = self.client.get_decision(diff)

        self.assertEqual(actual_decision, expected_decision)

class TestAzureClient(unittest.TestCase):
    def setUp(self):
        self.client = AzureClient("test_api_key", "test_model", "test_system_prompt", 0.5, "test_endpoint", "test_deployment_id")

    @patch("openai.ChatCompletion.create")
    def test_get_decision(self, mock_create):
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message={"content": '{"decision": "yes", "reason": "because."}'})]
        mock_create.return_value = mock_completion

        diff = "This is a test diff."
        expected_decision = {"decision": "yes", "reason": "because."}
        actual_decision = self.client.get_decision(diff)

        self.assertEqual(actual_decision, expected_decision)

    def test_attributes(self):
        self.assertEqual(openai.api_key, "test_api_key")
        self.assertEqual(self.client.model, "test_model")
        self.assertEqual(self.client.system_prompt, "test_system_prompt")
        self.assertEqual(self.client.temperature, 0.5)
        self.assertEqual(self.client.deployment_id, "test_deployment_id")