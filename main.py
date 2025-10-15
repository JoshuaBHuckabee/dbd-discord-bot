import asyncio
from config import DISCORD_TOKEN
from bot import create_bot

# Main function
async def main():
    bot = create_bot()
    async with bot:
        await bot.load_cogs()
        await bot.start(DISCORD_TOKEN)

# Only execute when the script is run directly
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot shutdown gracefully.")
