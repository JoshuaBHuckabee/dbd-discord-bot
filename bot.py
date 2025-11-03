# ------------------------------------------------------------
# Module: Discord Bot Factory
# ------------------------------------------------------------
# This module defines the bot creation logic for the Discord
# application. It sets up intents, command handling, event
# listeners, and dynamically loads all configured cogs.
#
# Exported Function:
# - create_bot(): Initializes and returns a configured bot
#   instance ready to connect to Discord.
# ------------------------------------------------------------

import discord
from discord.ext import commands
import asyncio
from config import COGS
import os
from rich.console import Console

# ------------------------------------------------------------
# Console Setup (Rich)
# ------------------------------------------------------------
# The Rich library provides colored console output for better
# visibility and debugging feedback during bot startup.
# ------------------------------------------------------------
console = Console()

# ------------------------------------------------------------
# Function: create_bot
# ------------------------------------------------------------
# Creates and configures the Discord bot instance.
# ------------------------------------------------------------
# - Sets up Discord intents (permissions for event listening)
# - Defines the "on_ready" event for startup confirmation
# - Defines a helper method "load_cogs" to dynamically load
#   all extensions defined in the COGS list
# ------------------------------------------------------------
def create_bot() -> commands.Bot:
    # Setup Discord intents (controls what events your bot can listen to)
    intents = discord.Intents.default()
    intents.message_content = True  # Required to read the content of messages

    # Initialize the bot instance with a command prefix and intents
    bot = commands.Bot(command_prefix="!", intents=intents)

    # --------------------------------------------------------
    # Event: on_ready
    # --------------------------------------------------------
    # Triggered when the bot successfully connects to Discord.
    # Displays login information and syncs slash commands.
    # --------------------------------------------------------
    @bot.event
    async def on_ready():
        console.print(f"[green][OK][/green] Logged in as {bot.user} ({bot.user.id})")
        try:
            synced = await bot.tree.sync()
            console.print(f"- Synced {len(synced)} slash command(s)")
        except Exception as e:
            console.print(f"[red]Error syncing commands: {e}")

    # --------------------------------------------------------
    # Async Function: load_cogs
    # --------------------------------------------------------
    # Loads all cogs (extensions) defined in the config file.
    # Displays success or error messages for each cog and adds
    # a short delay to make the Rich spinner visible.
    # --------------------------------------------------------
    async def load_cogs():
        with console.status(" Loading cogs...", spinner="dots") as status:
            for cog in COGS:
                try:
                    await bot.load_extension(cog)
                    console.print(f"[green][OK][/green] Loaded {cog}")
                except Exception as e:
                    console.print(f"[red] Failed to load {cog}: {e}")
                await asyncio.sleep(0.5)  # Small delay so spinner is visible

    # Attach the async function for external access
    bot.load_cogs = load_cogs

    return bot
