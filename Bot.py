# bot.py

import discord
from discord.ext import commands

# Set up Discord Intents to enable bot to receive message events
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read message content (needed for commands)

# Initialize bot with command prefix '!' and specified intents
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# prints a message when the bot is ready in the terminal.
@bot.event
async def on_ready():
    """Event: Called when the bot logs in successfully."""
    print(f'✅ Logged in as {bot.user}')

# !help command placeholder
@bot.command()
async def help(ctx):
    """Command: Lists all available bot commands."""
    help_message = (
        "**🤖 CuseBot Commands:**\n"
        "`!help` – Show this help message\n"
        "`!resume` – Link to engineering resume resources\n"
        "`!events` – See upcoming club events\n"
        "`!resources` – Get recommended CS learning materials\n"
    )
    await ctx.send(help_message)

# !resume command placeholder
@bot.command()
async def resume(ctx):
    """Command: Sends a link to resume resources."""
    await ctx.send(
        "📄 Resume Resources: https://www.reddit.com/r/EngineeringResumes/wiki/index/"
    )

# !events command placeholder
@bot.command()
async def events(ctx):
    """Command: Sends a list of upcoming events."""
    await ctx.send(
        "📅 Upcoming Events:\n"
        "- April 12: Git Workshop\n"
        "- April 19: LeetCode Challenge Night\n"
        "- April 26: Final Meeting + Pizza 🍕"
    )

# !resources command placeholder
@bot.command()
async def resources(ctx):
    """Command: Sends recommended CS learning resources."""
    await ctx.send(
        "📚 CS Learning Resources:\n"
        "- [CS50](https://cs50.harvard.edu)\n"
        "- [The Odin Project](https://www.theodinproject.com/)\n"
        "- [FreeCodeCamp](https://www.freecodecamp.org/)\n"
        "- [LeetCode](https://leetcode.com/)"
    )



if __name__ == "__main__":
    # Probably not the best way to do this, but it works for now
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
# to run the bot, run the command: python Bot.py in the folder containing the file. 
# make sure you have the discord.py library installed. 