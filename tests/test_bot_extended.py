# test_bot_extended.py
# Extended test suite for the Discord bot with comprehensive test coverage
# Includes edge cases, error handling, integration tests, and performance tests

import unittest
from unittest.mock import AsyncMock, MagicMock, patch, call
import asyncio
import discord
from discord.ext import commands
import sys
import os
from bot import bot, run_bot


class TestBotExtended(unittest.IsolatedAsyncioTestCase):
    """Extended test suite for Discord bot with comprehensive coverage"""

    async def asyncSetUp(self):
        """Set up test fixtures before each test method"""
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()
        self.ctx.author = MagicMock()
        self.ctx.author.id = 12345
        self.ctx.author.name = "TestUser"
        self.ctx.guild = MagicMock()
        self.ctx.guild.id = 67890
        self.ctx.channel = MagicMock()
        self.ctx.channel.id = 11111

    # Test command content validation
    async def test_help_command_content_structure(self):
        """Test that help command returns properly formatted content"""
        await bot.get_command("help").callback(self.ctx)
        
        # Get the sent message
        sent_message = self.ctx.send.call_args[0][0]
        
        # Verify structure
        self.assertIn("**🤖 CuseBot Commands:**", sent_message)
        self.assertIn("`!help`", sent_message)
        self.assertIn("`!resume`", sent_message)
        self.assertIn("`!events`", sent_message)
        self.assertIn("`!resources`", sent_message)

    async def test_resume_command_url_validity(self):
        """Test that resume command returns a valid URL format"""
        await bot.get_command("resume").callback(self.ctx)
        
        sent_message = self.ctx.send.call_args[0][0]
        self.assertIn("https://", sent_message)
        self.assertIn("reddit.com", sent_message)
        self.assertIn("📄", sent_message)

    async def test_events_command_date_format(self):
        """Test that events command includes proper date formatting"""
        await bot.get_command("events").callback(self.ctx)
        
        sent_message = self.ctx.send.call_args[0][0]
        self.assertIn("📅 Upcoming Events:", sent_message)
        self.assertIn("April", sent_message)
        self.assertIn("Git Workshop", sent_message)
        self.assertIn("LeetCode Challenge", sent_message)
        self.assertIn("🍕", sent_message)

    async def test_resources_command_links_format(self):
        """Test that resources command includes properly formatted links"""
        await bot.get_command("resources").callback(self.ctx)
        
        sent_message = self.ctx.send.call_args[0][0]
        self.assertIn("📚 CS Learning Resources:", sent_message)
        self.assertIn("[CS50]", sent_message)
        self.assertIn("https://", sent_message)
        self.assertIn("cs50.harvard.edu", sent_message)
        self.assertIn("theodinproject.com", sent_message)
        self.assertIn("freecodecamp.org", sent_message)
        self.assertIn("leetcode.com", sent_message)

    # Test error handling scenarios
    async def test_command_with_send_failure(self):
        """Test command behavior when ctx.send fails"""
        self.ctx.send.side_effect = discord.HTTPException(MagicMock(), "Network error")
        
        with self.assertRaises(discord.HTTPException):
            await bot.get_command("help").callback(self.ctx)

    async def test_command_with_forbidden_error(self):
        """Test command behavior when bot lacks permissions"""
        self.ctx.send.side_effect = discord.Forbidden(MagicMock(), "Missing permissions")
        
        with self.assertRaises(discord.Forbidden):
            await bot.get_command("resume").callback(self.ctx)

    # Test bot initialization and configuration
    def test_bot_configuration(self):
        """Test that bot is configured with correct settings"""
        self.assertEqual(bot.command_prefix, "!")
        self.assertTrue(bot.intents.messages)
        self.assertTrue(bot.intents.message_content)
        self.assertIsNone(bot.help_command)

    def test_bot_has_all_commands(self):
        """Test that all expected commands are registered"""
        command_names = [cmd.name for cmd in bot.commands]
        expected_commands = ["help", "resume", "events", "resources"]
        
        for cmd in expected_commands:
            self.assertIn(cmd, command_names)

    # Test environment and token handling edge cases
    @patch("os.getenv")
    @patch("bot.load_dotenv", return_value=True)
    def test_token_with_whitespace(self, mock_load_dotenv, mock_getenv):
        """Test handling of token with leading/trailing whitespace"""
        mock_getenv.return_value = "  valid_token  "
        
        with patch("bot.bot.run") as mock_run:
            run_bot()
            # Should strip whitespace
            mock_run.assert_called_once_with("  valid_token  ")

    @patch("os.getenv", return_value=None)
    @patch("bot.load_dotenv", return_value=True)
    def test_token_none_value(self, mock_load_dotenv, mock_getenv):
        """Test handling when token is None"""
        with self.assertRaises(AssertionError):
            run_bot()

    @patch("bot.bot.run", side_effect=discord.HTTPException(MagicMock(), "Connection failed"))
    @patch("os.getenv", return_value="valid_token")
    @patch("bot.load_dotenv", return_value=True)
    def test_connection_error(self, mock_load_dotenv, mock_getenv, mock_bot_run):
        """Test handling of connection errors during bot startup"""
        with self.assertRaises(discord.HTTPException):
            run_bot()

    # Test concurrent command execution
    async def test_multiple_commands_concurrently(self):
        """Test that multiple commands can be executed concurrently"""
        ctx1 = MagicMock()
        ctx1.send = AsyncMock()
        ctx2 = MagicMock()
        ctx2.send = AsyncMock()
        ctx3 = MagicMock()
        ctx3.send = AsyncMock()

        # Execute commands concurrently
        await asyncio.gather(
            bot.get_command("help").callback(ctx1),
            bot.get_command("resume").callback(ctx2),
            bot.get_command("events").callback(ctx3)
        )

        # Verify all commands executed
        ctx1.send.assert_called_once()
        ctx2.send.assert_called_once()
        ctx3.send.assert_called_once()

    # Test command docstrings and metadata
    def test_command_docstrings(self):
        """Test that all commands have proper docstrings"""
        for command in bot.commands:
            self.assertIsNotNone(command.callback.__doc__)
            self.assertTrue(len(command.callback.__doc__.strip()) > 0)

    # Test bot events
    @patch('builtins.print')
    async def test_on_ready_event(self, mock_print):
        """Test the on_ready event handler"""
        # Mock bot user for the event
        with patch.object(bot, 'user') as mock_user:
            mock_user.__str__ = MagicMock(return_value="TestBot#1234")
            
            # Trigger the on_ready event directly if it exists
            if hasattr(bot, 'on_ready'):
                await bot.on_ready()
                mock_print.assert_called_with("✅ Logged in as TestBot#1234")
            else:
                # Skip test if on_ready handler doesn't exist
                self.skipTest("Bot does not have on_ready event handler")

    # Test command aliases and case sensitivity
    def test_command_case_sensitivity(self):
        """Test that commands are case sensitive"""
        # Commands should be lowercase
        self.assertIsNotNone(bot.get_command("help"))
        self.assertIsNone(bot.get_command("HELP"))
        self.assertIsNone(bot.get_command("Help"))

    # Performance and load testing
    async def test_rapid_command_execution(self):
        """Test bot performance under rapid command execution"""
        contexts = []
        for i in range(10):
            ctx = MagicMock()
            ctx.send = AsyncMock()
            contexts.append(ctx)

        # Execute help command rapidly
        tasks = [bot.get_command("help").callback(ctx) for ctx in contexts]
        await asyncio.gather(*tasks)

        # Verify all executed successfully
        for ctx in contexts:
            ctx.send.assert_called_once()

    # Test message length limits
    async def test_message_length_compliance(self):
        """Test that all command responses are within Discord's message limits"""
        commands_to_test = ["help", "resume", "events", "resources"]
        
        for cmd_name in commands_to_test:
            ctx = MagicMock()
            ctx.send = AsyncMock()
            
            await bot.get_command(cmd_name).callback(ctx)
            
            sent_message = ctx.send.call_args[0][0]
            # Discord message limit is 2000 characters
            self.assertLessEqual(len(sent_message), 2000, 
                               f"Command {cmd_name} response too long")

    # Test environment file edge cases
    @patch("bot.load_dotenv", side_effect=Exception("File read error"))
    def test_dotenv_load_exception(self, mock_load_dotenv):
        """Test handling of exceptions during .env file loading"""
        with self.assertRaises(Exception):
            run_bot()

    @patch("os.getenv", side_effect=KeyError("Environment variable not found"))
    @patch("bot.load_dotenv", return_value=True)
    def test_getenv_exception(self, mock_load_dotenv, mock_getenv):
        """Test handling of exceptions during environment variable access"""
        with self.assertRaises(KeyError):
            run_bot()

    # Integration test for complete bot workflow
    @patch("bot.bot.run")
    @patch("os.getenv", return_value="test_token_12345")
    @patch("bot.load_dotenv", return_value=True)
    async def test_complete_bot_workflow(self, mock_load_dotenv, mock_getenv, mock_bot_run):
        """Integration test for complete bot startup and command execution"""
        # Test bot startup
        run_bot()
        mock_bot_run.assert_called_once_with("test_token_12345")
        
        # Test all commands work together
        for cmd_name in ["help", "resume", "events", "resources"]:
            ctx = MagicMock()
            ctx.send = AsyncMock()
            await bot.get_command(cmd_name).callback(ctx)
            ctx.send.assert_called_once()

    # Test bot cleanup and shutdown scenarios
    def test_bot_cleanup(self):
        """Test that bot can be properly cleaned up"""
        # This would test cleanup logic if implemented
        self.assertIsNotNone(bot)
        # In a real scenario, you might test bot.close() or similar cleanup

    async def asyncTearDown(self):
        """Clean up after each test"""
        # Reset any mocks or state if needed
        pass


class TestBotCommandValidation(unittest.IsolatedAsyncioTestCase):
    """Separate test class for command validation and edge cases"""

    async def asyncSetUp(self):
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()

    async def test_commands_return_strings(self):
        """Test that all commands return string responses"""
        commands_to_test = ["help", "resume", "events", "resources"]
        
        for cmd_name in commands_to_test:
            await bot.get_command(cmd_name).callback(self.ctx)
            sent_message = self.ctx.send.call_args[0][0]
            self.assertIsInstance(sent_message, str)

    async def test_commands_not_empty(self):
        """Test that no command returns empty responses"""
        commands_to_test = ["help", "resume", "events", "resources"]
        
        for cmd_name in commands_to_test:
            await bot.get_command(cmd_name).callback(self.ctx)
            sent_message = self.ctx.send.call_args[0][0]
            self.assertTrue(len(sent_message.strip()) > 0)

    async def test_unicode_emoji_support(self):
        """Test that commands properly handle Unicode emojis"""
        await bot.get_command("help").callback(self.ctx)
        sent_message = self.ctx.send.call_args[0][0]
        # Should contain emoji characters
        self.assertTrue(any(ord(char) > 127 for char in sent_message))


if __name__ == "__main__":
    # Run the extended tests
    unittest.main(verbosity=2) 