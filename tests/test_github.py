import unittest
from unittest.mock import patch, mock_open
import os
import sys
from src.utils.github import EventContext

# Super hacky way to import modules from the src directory because I cant figure out how the f to use unit tests properly
sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src/utils")


class TestEventContext(unittest.TestCase):
    def setUp(self):
        with patch("builtins.open", mock_open(read_data='{"action": "synchronize", "pull_request": {"diff_url": "test_diff_url", "comments_url": "test_comment_url"}}')):
            self.context = EventContext()

    @patch("builtins.open", mock_open(read_data='{"action": "synchronize", "pull_request": {"diff_url": "test_diff_url", "comments_url": "test_comment_url"}}'))
    def test_get_action_context_pull_request(self):
        self.context._EventContext__get_action_context()

        self.assertEqual(self.context.action, "synchronize")
        self.assertEqual(self.context.diff_url, "test_diff_url")
        self.assertEqual(self.context.comment_url, "test_comment_url")

    @patch("builtins.open", mock_open(read_data='{"compare": "test_compare_url"}'))
    def test_get_action_context_commit(self):
        self.context._EventContext__get_action_context()

        self.assertEqual(self.context.action, "commit")
        self.assertEqual(self.context.diff_url, "test_compare_url.diff")

    def test_get_env_vars(self):
        with patch.dict("os.environ", {
            "INPUT_GH_TOKEN": "test_gh_token",
            "INPUT_MODEL": "test_model",
            "INPUT_OPENAI_API_KEY": "test_openai_api_key",
            "INPUT_AZURE_API_KEY": "test_azure_api_key",
            "INPUT_AZURE_ENDPOINT": "test_azure_endpoint",
            "INPUT_AZURE_DEPLOYMENT_ID": "test_azure_deployment_id",
        }):
            expected_vars = {
                "gh_token": "test_gh_token",
                "model": "test_model",
                "openai_api_key": "test_openai_api_key",
                "azure_api_key": "test_azure_api_key",
                "azure_endpoint": "test_azure_endpoint",
                "azure_deployment_id": "test_azure_deployment_id",
            }
            actual_vars = self.context._EventContext__get_env_vars()

            self.assertEqual(actual_vars, expected_vars)

    def test_validate_inputs_both_empty(self):
        self.context.vars = {
            "openai_api_key": None,
            "azure_api_key": None,
            "azure_endpoint": None,
            "azure_deployment_id": None,
        }

        with self.assertRaises(Exception):
            self.context.validate_inputs()

    def test_validate_inputs_both_set(self):
        self.context.vars = {
            "openai_api_key": "test_openai_api_key",
            "azure_api_key": "test_azure_api_key",
            "azure_endpoint": None,
            "azure_deployment_id": None,
        }

        with self.assertRaises(Exception):
            self.context.validate_inputs()

    def test_validate_inputs_azure_missing(self):
        self.context.vars = {
            "openai_api_key": None,
            "azure_api_key": "test_azure_api_key",
            "azure_endpoint": "test_azure_endpoint",
            "azure_deployment_id": None,
        }

        with self.assertRaises(Exception):
            self.context.validate_inputs()

    def test_validate_inputs_azure_missing_values(self):
        self.context.vars = {
            "openai_api_key": None,
            "azure_api_key": "test_azure_api_key",
            "azure_endpoint": None,
            "azure_deployment_id": None,
        }

        with self.assertRaises(Exception):
            self.context.validate_inputs()

    def test_validate_inputs_valid(self):
        self.context.vars = {
            "openai_api_key": "test_openai_api_key",
            "azure_api_key": None,
            "azure_endpoint": None,
            "azure_deployment_id": None,
        }

        self.context.validate_inputs()

if __name__ == "__main__":
    unittest.main()