import unittest
from unittest.mock import patch, Mock, mock_open
import os
import sys
from src.utils.github import EventContext, API

# Super hacky way to import modules from the src directory because I cant figure out how the f to use unit tests properly
sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src/utils")


class TestEventContext(unittest.TestCase):
    def setUp(self):
        with patch("builtins.open", mock_open(read_data='{"action": "synchronize", "pull_request": {"url": "test_url", "comments_url": "test_comment_url"}}')):
            self.context = EventContext()

    @patch("builtins.open", mock_open(read_data='{"action": "synchronize", "pull_request": {"url": "test_url", "comments_url": "test_comment_url"}}'))
    def test_get_action_context_pull_request(self):
        self.context._EventContext__get_action_context()

        self.assertEqual(self.context.action, "synchronize")
        self.assertEqual(self.context.url, "test_url")
        self.assertEqual(self.context.comment_url, "test_comment_url")

    @patch("builtins.open", mock_open(read_data='{"compare": "test_compare_url"}'))
    def test_get_action_context_commit(self):
        self.context._EventContext__get_action_context()

        self.assertEqual(self.context.action, None)

    @patch("builtins.open", mock_open(read_data='{"action": "labeled", "pull_request": {"url": "test_url", "comments_url": "test_comment_url"}}'))
    def test_get_action_context_label(self):
        self.context._EventContext__get_action_context()

        self.assertEqual(self.context.action, None)

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


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.token = "test_token"
        self.api = API(self.token)

    @patch("requests.get")
    def test_get_diff_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "test_diff"
        mock_get.return_value = mock_response

        compare_url = "test_compare_url"
        diff = self.api.get_diff(compare_url)

        self.assertEqual(diff, "test_diff")
        mock_get.assert_called_once_with(compare_url, headers=self.api.diff_headers)

    @patch("requests.get")
    def test_get_diff_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        compare_url = "test_compare_url"

        with self.assertRaises(Exception):
            self.api.get_diff(compare_url)

        mock_get.assert_called_once_with(compare_url, headers=self.api.diff_headers)

    @patch("requests.post")
    def test_add_comment_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        comment_url = "test_comment_url"
        comment = "test_comment"

        self.api.add_comment(comment_url, comment)

        mock_post.assert_called_once_with(comment_url, headers=self.api.headers, json={"body": comment})

    @patch("requests.post")
    def test_add_comment_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad Request"}
        mock_post.return_value = mock_response

        comment_url = "test_comment_url"
        comment = "test_comment"

        with self.assertRaises(Exception):
            self.api.add_comment(comment_url, comment)

        mock_post.assert_called_once_with(comment_url, headers=self.api.headers, json={"body": comment})

if __name__ == "__main__":
    unittest.main()