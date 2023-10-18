# import unittest
# import sys
# import logging
# import io
# from unittest.mock import patch, mock_open

# from src.smart_scan.smart_scan import main
# from src.utils import *

# # class TestGetInputs(unittest.TestCase):
# #     @patch('sys.argv', ["", "gh_token", "model", "openai_api_key", "", "azure_endpoint"])
# #     @patch('logging.error')
# #     def test_get_inputs(self, mock_logging):
# #         inputs = get_inputs()
# #         self.assertEqual(inputs["gh_token"], "gh_token")
# #         self.assertEqual(inputs["openai_api_key"], "openai_api_key")
# #         self.assertIsNone(inputs["azure_api_key"])
# #         self.assertEqual(inputs["azure_endpoint"], "azure_endpoint")
# #         mock_logging.assert_not_called()

# #     @patch('sys.argv', ["", "", "", "", "", ""])
# #     @patch('logging.error')
# #     def test_get_inputs_no_keys(self, mock_logging):
# #         with self.assertRaises(SystemExit) as cm:
# #             get_inputs()
# #         self.assertEqual(cm.exception.code, 1)
# #         mock_logging.assert_called_once_with("Both openai_api_key and azure_api_key are empty. Exiting.")

# #     @patch('sys.argv', ["", "gh_token", "model", "openai_api_key", "azure_api_key", "azure_endpoint"])
# #     @patch('logging.error')
# #     def test_get_inputs_both_keys(self, mock_logging):
# #         with self.assertRaises(SystemExit) as cm:
# #             get_inputs()
# #         self.assertEqual(cm.exception.code, 1)
# #         mock_logging.assert_called_once_with("Both openai_api_key and azure_api_key are set. Exiting.")

# # class TestGetConfig(unittest.TestCase):
# #     def test_get_config(self):
# #         # Test case for a valid YAML file
# #         with patch('builtins.open', return_value=io.StringIO("name: test\nversion: 1.0")):
# #             config = get_config("config.yaml")
# #             self.assertEqual(config, {"name": "test", "version": 1.0})

# #         # Test case for an invalid YAML file
# #         with patch('builtins.open', return_value=io.StringIO("name: test\nversion: 1.0\ninvalid")):
# #             with self.assertRaises(SystemExit) as cm:
# #                 get_config("config.yaml")
# #             self.assertEqual(cm.exception.code, 1)

# #         # Test case for a non-existent file
# #         with self.assertRaises(FileNotFoundError):
# #             get_config("nonexistent.yaml")

# # class TestGetEventContext(unittest.TestCase):
# #     @patch('builtins.open', mock_open(read_data='{"action": "synchronize", "pull_request": {"diff_url": "https://github.com/user/repo/pull/123.diff", "comments_url": "https://github.com/user/repo/pull/123/comments"}}'))
# #     def test_get_event_context_pull_request_synchronize(self):
# #         ctx = get_event_context()
# #         self.assertEqual(ctx["action"], "synchronize")
# #         self.assertEqual(ctx["diff_url"], "https://github.com/user/repo/pull/123.diff")
# #         self.assertEqual(ctx["comment_url"], "https://github.com/user/repo/pull/123/comments")

# #     @patch('builtins.open', mock_open(read_data='{"action": "opened", "pull_request": {"diff_url": "https://github.com/user/repo/pull/123.diff", "comments_url": "https://github.com/user/repo/pull/123/comments"}}'))
# #     def test_get_event_context_pull_request_opened(self):
# #         ctx = get_event_context()
# #         self.assertEqual(ctx["action"], "opened")
# #         self.assertEqual(ctx["diff_url"], "https://github.com/user/repo/pull/123.diff")
# #         self.assertEqual(ctx["comment_url"], "https://github.com/user/repo/pull/123/comments")

# #     @patch('builtins.open', mock_open(read_data='{"compare": "https://github.com/user/repo/compare/abc123...def456"}'))
# #     def test_get_event_context_commit(self):
# #         ctx = get_event_context()
# #         self.assertEqual(ctx["action"], "commit")
# #         self.assertEqual(ctx["diff_url"], "https://github.com/user/repo/compare/abc123...def456.diff")

# # class TestSetActionOutput(unittest.TestCase):
# #     def test_set_action_output_writes_to_file(self):
# #         os.environ["GITHUB_OUTPUT"] = "test_output.txt"
# #         set_action_output("test_value")
# #         with open("test_output.txt", "r") as f:
# #             contents = f.read()
# #         self.assertIn("decision=test_value", contents)
# #         os.remove("test_output.txt")
# print("hey")
# if __name__ == '__main__':
#     unittest.main()