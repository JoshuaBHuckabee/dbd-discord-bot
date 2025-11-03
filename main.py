# ------------------------------------------------------------
# Entry Point: Discord Bot
# ------------------------------------------------------------
# This script initializes and runs the Discord bot.
# It loads all bot cogs (extensions), connects using the
# Discord token, and starts the event loop.
#
# When run directly, it executes the async main() function
# and ensures a graceful shutdown on keyboard interrupt.
# ------------------------------------------------------------

import asyncio
from config import DISCORD_TOKEN
from bot import create_bot

# ------------------------------------------------------------
# Main Async Function
# ------------------------------------------------------------
# - Creates an instance of the bot using create_bot()
# - Loads all bot cogs before connecting
# - Starts the bot with the provided Discord token
# ------------------------------------------------------------
async def main():
    bot = create_bot()
    async with bot:
        await bot.load_cogs()
        await bot.start(DISCORD_TOKEN)

# ------------------------------------------------------------
# Script Entrypoint
# ------------------------------------------------------------
# Ensures this script only runs when executed directly.
# Handles KeyboardInterrupt (Ctrl+C) for a clean shutdown.
# ------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot shutdown gracefully.")
