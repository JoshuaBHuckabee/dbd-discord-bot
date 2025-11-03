import os
import random
import asyncio
import discord
from discord.ext import commands
from config import SACRIFICIAL_TERMINAL_CHANNEL_ID

# Define a Cog class that represents the bot's startup functionality
class Startup(commands.Cog):
    def __init__(self, bot):
        # Initialize with the bot instance
        self.bot = bot
        # Schedule the startup_task co-routine to run as soon as the bot starts up
        self.bot.loop.create_task(self.startup_task())

    async def startup_task(self):
        # Wait until the bot has fully initialized and is ready
        await self.bot.wait_until_ready()

        # If the startup message has already been sent, exit the function
        if getattr(self.bot, "startup_message_sent", False):
            return

        # Mark that the startup message has been sent to prevent it from being sent again
        self.bot.startup_message_sent = True

        # Get the channel where the message will be sent using the channel ID
        channel = self.bot.get_channel(SACRIFICIAL_TERMINAL_CHANNEL_ID)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(SACRIFICIAL_TERMINAL_CHANNEL_ID)
            except Exception:
                # If fetching the channel fails, exit the function
                return

        # If the channel was successfully retrieved or fetched
        if channel:
            # Random footers for embed
            footers = [
                "Use commands wisely... not all who summon survive.",
                "The Fog watches.",
                "The Entity stirs. Obey, or be consumed.",
                "Not every trial ends in escape...",
            ]

            # Create the embed
            embed = discord.Embed(
                title="🩸 The Fog Stirs...",
                description="*A cold presence drifts through the realm... The Entity has awakened.*",
                color=discord.Color.dark_red(),
                timestamp=discord.utils.utcnow()
            )

            # Set Author displays for embed
            embed.set_author(
                name="The Entity",
                icon_url="https://i1.sndcdn.com/artworks-plRLOcmkI3LEe7Nc-ak5LYQ-t500x500.jpg",
                url="https://deadbydaylight.fandom.com/wiki/The_Entity"
            )

            # Set the menu for the embed
            embed.add_field(name="`/ping`", value="Ping the Entity", inline=False)
            embed.add_field(name="`/glyph`", value="Reveal glyph types, colors, and roles (slash command coming soon!)", inline=False)
            embed.add_field(name="`/lore`", value="Receive fragments of forgotten knowledge", inline=False)
            embed.add_field(name="`/events`", value="Shows current and upcoming Dead by Daylight in-game events, including dates, rewards, and special features.", inline=False)
            embed.add_field(name="`/players`", value="Reveal how many are currently trapped in the Fog...", inline=False)
            embed.add_field(name="`!killer`", value="Coming Soon!", inline=False)

            # Add empty field for spacing (2 line breaks visually)
            embed.add_field(name="\u200b", value="\u200b", inline=False)

            # Set random footer
            embed.set_footer(text=random.choice(footers))

            # Send primary embed
            await channel.send(embed=embed)

            # Delayed atmospheric follow-up
            await asyncio.sleep(6)

            # Random fog lines to be sent after startup message is posted
            fog_lines = [
                "🌩 *A crack of thunder echoes in the distance...*",
                "🌫 *The Fog thickens. A trial is about to begin.*",
                "🕯 *A candle flickers... then vanishes.*",
                "🪦 *Something ancient stirs beneath the surface...*"
            ]

            # Send a random fog line
            await channel.send(random.choice(fog_lines))

# This function is required to add the cog to the bot when it's loaded
async def setup(bot):
    await bot.add_cog(Startup(bot))
