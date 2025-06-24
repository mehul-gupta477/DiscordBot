import unittest
import sys
from unittest.mock import patch, mock_open, MagicMock


class TestNotifyDiscord(unittest.TestCase):

    def setUp(self):
        # Remove the module if it was already imported to ensure clean import
        if "notify_discord" in sys.modules:
            del sys.modules["notify_discord"]
    
    def tearDown(self):
        # Ensure notify_discord is removed after each test
        sys.modules.pop("notify_discord", None)

    @patch("requests.post")
    def test_successful_post_to_discord(self, mock_post):
        # Mock successful HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Mock environment variables and file operations
        with patch("os.getenv") as mock_getenv, patch(
            "builtins.open", mock_open()
        ) as mock_file:

            def getenv_side_effect(key):
                env_vars = {
                    "GITHUB_EVENT_NAME": "issues",
                    "GITHUB_EVENT_PATH": "event.json",
                    "DISCORD_WEBHOOK_URL": "https://fake.webhook.url",
                }
                return env_vars.get(key)

            mock_getenv.side_effect = getenv_side_effect

            # Mock event.json and user_map.json files
            event_data = '{"action": "opened", "issue": {"title": "Test Issue", "html_url": "https://github.com/test", "assignees": []}}'
            user_map_data = '{"user1": "123456789"}'

            mock_file.side_effect = [
                mock_open(read_data=event_data).return_value,
                mock_open(read_data=user_map_data).return_value,
            ]

            # Import the module after mocking
            import notify_discord

            # Test the function
            notify_discord.post_to_discord("Test Message")

            # Verify the request was made
            mock_post.assert_called_once_with(
                "https://fake.webhook.url", json={"content": "Test Message"}
            )

    def test_missing_github_event_name(self):
        # Mock environment variables without event name
        with patch("os.getenv") as mock_getenv, patch(
            "builtins.open", mock_open(read_data='{"user1": "123456789"}')
        ):

            def getenv_side_effect(key):
                env_vars = {
                    "GITHUB_EVENT_NAME": None,
                    "GITHUB_EVENT_PATH": "event.json",
                    "DISCORD_WEBHOOK_URL": "https://fake.webhook.url",
                }
                return env_vars.get(key)

            mock_getenv.side_effect = getenv_side_effect

            # Test that ValueError is raised when event name is missing
            with self.assertRaises(ValueError) as context:
                import notify_discord

            self.assertIn(
                "GITHUB_EVENT_NAME environment variable is not set",
                str(context.exception),
            )

    def test_missing_github_event_path(self):
        # Mock environment variables without event path
        with patch("os.getenv") as mock_getenv, patch(
            "builtins.open", mock_open(read_data='{"user1": "123456789"}')
        ):

            def getenv_side_effect(key):
                env_vars = {
                    "GITHUB_EVENT_NAME": "issues",
                    "GITHUB_EVENT_PATH": None,
                    "DISCORD_WEBHOOK_URL": "https://fake.webhook.url",
                }
                return env_vars.get(key)

            mock_getenv.side_effect = getenv_side_effect

            # Test that ValueError is raised when event path is missing
            with self.assertRaises(ValueError) as context:
                import notify_discord

            self.assertIn(
                "GITHUB_EVENT_PATH environment variable is not set",
                str(context.exception),
            )

    def test_missing_discord_webhook_url(self):
        # Mock environment variables without webhook URL
        with patch("os.getenv") as mock_getenv, patch(
            "builtins.open", mock_open()
        ) as mock_file:

            def getenv_side_effect(key):
                env_vars = {
                    "GITHUB_EVENT_NAME": "issues",
                    "GITHUB_EVENT_PATH": "event.json",
                    "DISCORD_WEBHOOK_URL": None,
                }
                return env_vars.get(key)

            mock_getenv.side_effect = getenv_side_effect

            # Mock event.json and user_map.json files
            event_data = '{"action": "opened", "issue": {"title": "Test Issue", "html_url": "https://github.com/test", "assignees": []}}'
            user_map_data = '{"user1": "123456789"}'

            mock_file.side_effect = [
                mock_open(read_data=event_data).return_value,
                mock_open(read_data=user_map_data).return_value,
            ]

            # Test that ValueError is raised during module import
            with self.assertRaises(ValueError) as context:
                import notify_discord

            self.assertIn(
                "DISCORD_WEBHOOK_URL environment variable is missing or empty.",
                str(context.exception),
            )

    @patch("requests.post")
    def test_post_to_discord_function_with_missing_webhook(self, mock_post):
        # Test the actual function behavior when webhook_url is None
        with patch("os.getenv") as mock_getenv, patch(
            "builtins.open", mock_open()
        ) as mock_file:

            def getenv_side_effect(key):
                env_vars = {
                    "GITHUB_EVENT_NAME": "issues",
                    "GITHUB_EVENT_PATH": "event.json",
                    "DISCORD_WEBHOOK_URL": "https://fake.webhook.url",  # Set valid URL for import
                }
                return env_vars.get(key)

            mock_getenv.side_effect = getenv_side_effect

            # Mock event.json and user_map.json files
            event_data = '{"action": "opened", "issue": {"title": "Test Issue", "html_url": "https://github.com/test", "assignees": []}}'
            user_map_data = '{"user1": "123456789"}'

            mock_file.side_effect = [
                mock_open(read_data=event_data).return_value,
                mock_open(read_data=user_map_data).return_value,
            ]

            # Import the module
            import notify_discord

            # Now manually test the function with a None webhook_url by patching the module's webhook_url
            with patch.object(notify_discord, "webhook_url", None):
                with self.assertRaises(ValueError) as context:
                    notify_discord.post_to_discord("Test Message")

                self.assertIn(
                    "DISCORD_WEBHOOK_URL environment variable is not set",
                    str(context.exception),
                )
                mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
