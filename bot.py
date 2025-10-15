import discord
from discord.ext import commands
import asyncio
from config import COGS
import os


# Setup Discord intents (controls what events your bot can listen to)
def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True # Required to read the content of messages

    # Initialize the bot instance with a command prefix and intents
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Event triggered when the bot is ready and connected to Discord
    @bot.event
    async def on_ready():
        print(f"✅ Logged in as {bot.user} ({bot.user.id})")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} slash command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    # Asynchronously load all bot extensions (cogs)
    async def load_cogs():
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")

    bot.load_cogs = load_cogs  # Attach for external access

    return bot

