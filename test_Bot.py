# test_bot.py
# This file contains unit tests for the Discord bot commands
# It uses Python's unittest framework with async support for testing Discord.py commands

import unittest
from unittest.mock import AsyncMock, MagicMock
from Bot import bot  # Import the bot instance directly

class TestCSClubBot(unittest.IsolatedAsyncioTestCase):
    """Test suite for the CS Club Discord Bot commands"""

    async def asyncSetUp(self):
        """Set up test fixtures before each test method
        Creates a mock context that simulates Discord's message context"""
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()  # Mock the send method to test message sending

    async def test_help_command(self):
        """Test the !help command
        Verifies that:
        1. The command responds with a message
        2. The response includes information about the !resume command"""
        await bot.get_command('help').callback(self.ctx)
        self.ctx.send.assert_called()
        self.assertIn("!resume", self.ctx.send.call_args[0][0])

    async def test_resume_command(self):
        """Test the !resume command
        Verifies that the command returns the correct engineering resume resources URL"""
        await bot.get_command('resume').callback(self.ctx)
        self.ctx.send.assert_called_with(
            "📄 Resume Resources: https://www.reddit.com/r/EngineeringResumes/wiki/index/"
        )

    async def test_events_command(self):
        """Test the !events command
        Verifies that:
        1. The command responds with a message
        2. The response includes information about the Git Workshop"""
        await bot.get_command('events').callback(self.ctx)
        self.ctx.send.assert_called()
        self.assertIn("Git Workshop", self.ctx.send.call_args[0][0])

    async def test_resources_command(self):
        """Test the !resources command
        Verifies that:
        1. The command responds with a message
        2. The response includes FreeCodeCamp in the learning resources"""
        await bot.get_command('resources').callback(self.ctx)
        self.ctx.send.assert_called()
        self.assertIn("FreeCodeCamp", self.ctx.send.call_args[0][0])


if __name__ == "__main__":
    # Run the tests when the file is executed directly
    unittest.main()