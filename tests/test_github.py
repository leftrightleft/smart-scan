import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys
import src.utils.github as github

# Super hacky way to import modules from the src directory because I cant figure out how the f to use unit tests properly
sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src/utils")


class TestEventContext(unittest.TestCase):
    @patch("src.utils.github.EventContext.__get_action_context", MagicMock(return_value={"action": "synchronize"}))
    def test_validate_inputs_both_keys_set(self):
        ctx = github.EventContext()
        ctx.vars = {"openai_api_key": "openai_key", "azure_api_key": "azure_key"}
        with self.assertRaises(Exception):
            ctx.validate_inputs()

    @patch("src.utils.github.EventContext.__get_action_context", MagicMock(return_value={"action": "synchronize"}))
    def test_validate_inputs_both_keys_empty(self):
        ctx = github.EventContext()
        ctx.vars = {"openai_api_key": None, "azure_api_key": None}
        with self.assertRaises(Exception):
            ctx.validate_inputs()

    @patch("src.utils.github.EventContext.__get_action_context", MagicMock(return_value={"action": "synchronize"}))
    def test_validate_inputs_openai_key_set(self):
        ctx = github.EventContext()
        ctx.vars = {"openai_api_key": "openai_key", "azure_api_key": None}
        ctx.validate_inputs()

    @patch("src.utils.github.EventContext.__get_action_context", MagicMock(return_value={"action": "synchronize"}))
    def test_validate_inputs_azure_key_set(self):
        ctx = github.EventContext()
        ctx.vars = {"openai_api_key": None, "azure_api_key": "azure_key"}
        ctx.validate_inputs()
    # @patch("builtins.open", MagicMock(return_value=MagicMock(read=MagicMock(return_value=b'{"action": "synchronize"}'))))
    # def test_get_action_context(self):
    #     ctx = github.EventContext()
    #     ctx.__get_action_context()
    #     self.assertEqual(ctx.action, "synchronize")
    # def setUp(self):
    #     self.event_json = {
    #         "action": "synchronize",
    #         "pull_request": {
    #             "diff_url": "https://github.com/user/repo/pull/123.diff",
    #             "comments_url": "https://github.com/user/repo/pull/123/comments",
    #         },
    #     }
    #     self.env_vars = {
    #         "INPUT_OPENAI_API_KEY": "openai_key",
    #         "INPUT_AZURE_API_KEY": None,
    #     }

    # @patch("github.os")
    # def test_get_env_vars(self, mock_os):
    #     mock_os.environ = self.env_vars
    #     ctx = github.EventContext()
    #     self.assertEqual(ctx.vars, self.env_vars)

    # @patch("github.os")
    # def test_get_action_context_pull_request(self, mock_os):
    #     mock_os.environ = self.env_vars
    #     with patch("builtins.open", MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(self.event_json))))):
    #         ctx = github.EventContext()
    #     self.assertEqual(ctx.action, "synchronize")
    #     self.assertEqual(ctx.diff_url, "https://github.com/user/repo/pull/123.diff")
    #     self.assertEqual(ctx.comment_url, "https://github.com/user/repo/pull/123/comments")

    # # @patch("github.os")
    # # def test_get_action_context_commit(self, mock_os):
    # #     mock_os.environ = self.env_vars
    # #     event_json = {"compare": "https://github.com/user/repo/compare/abc123...def456"}
    # #     with patch("builtins.open", MagicMock(return_value=MagicMock(read=MagicMock(return_value=json.dumps(event_json))))):
    # #         ctx = github.EventContext()
    # #     self.assertEqual(ctx.action, "commit")
    # #     self.assertEqual(ctx.diff_url, "https://github.com/user/repo/compare/abc123...def456.diff")

    # def test_validate_inputs_both_keys_set(self):
    #     env_vars = {"INPUT_OPENAI_API_KEY": "openai_key", "INPUT_AZURE_API_KEY": "azure_key"}
    #     with self.assertRaises(Exception):
    #         ctx = github.EventContext()
    #         ctx.vars = env_vars
    #         ctx.validate_inputs()

    # def test_validate_inputs_both_keys_empty(self):
    #     env_vars = {"INPUT_OPENAI_API_KEY": None, "INPUT_AZURE_API_KEY": None}
    #     with self.assertRaises(Exception):
    #         ctx = github.EventContext()
    #         ctx.vars = env_vars
    #         ctx.validate_inputs()

if __name__ == "__main__":
    unittest.main()