import unittest
from unittest.mock import patch
from notify_discord import (
    post_to_discord,
    # generate_developer_list,
    # notify_assignment,
    # notify_review_request,
    # notify_review_state_change,
    # notify_comment_mention
)

class TestPostToDiscord(unittest.TestCase):

    @patch("builtins.open")
    @patch("os.getenv")
    @patch("requests.post")
    def test_successful_post_to_discord(self, mock_post, mock_getenv, mock_open):
        mock_getenv.side_effect = lambda key: {
            "GITHUB_EVENT_NAME": "issues",
            "GITHUB_EVENT_PATH": "event.json",
            "DISCORD_WEBHOOK_URL": "https://fake.webhook.url"
        }.get(key, "")

        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status.return_value = None

        from notify_discord import post_to_discord
        post_to_discord("Test Message")
        mock_post.assert_called_once()

