# cogs/core.py
import discord
import requests
import random
from discord.ext import commands
from discord import app_commands

# Define a Cog class to contain the core commands of the bot
class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # Store the bot instance for use in commands

    # Define a slash command: /ping
    @app_commands.command(name="ping", description="Ping the Entity")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong from the Fog!")

    # Define a slash command: /players
    @app_commands.command(name="players", description="How many players are active on steam?")
    async def players(self, interaction: discord.Interaction):
        # Steam API URL for getting current player count of Dead by Daylight (appid: 381210)
        url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=381210"
        try:
            # Make a GET request to the Steam API with a timeout
            response = requests.get(url, timeout=5)
            # Extract number number of players from API response
            count = response.json()['response']['player_count']
            await interaction.response.send_message(f"The Fog holds **{count:,}** survivors and killers in its grasp...")
        except Exception:
            # If error, send a failure message
            await interaction.response.send_message("The Entity cannot sense the numbers at this time...")

    # Define a slash command: /lore
    @app_commands.command(name="lore", description="Fragments... pieced together.")
    async def lore(self, interaction: discord.Interaction):
        # List of random "lore" fragments
        lore_fragments = [
            "The Entity watches all, feeding on the suffering of the lost.",
            "Whispers in the fog tell of survivors who once bargained with The Entity.",
            "Glyphs appear to those marked, guiding or deceiving their fate.",
            "Each trial is a story, written in pain and shadow.",
            "The Entity’s realm bends reality, warping hope and despair alike.",
            "Some say the Entity’s hunger can never be sated."
        ]

        # Create the embed message with a random lore fragment
        embed = discord.Embed(
            title="A Fragment of the Entity's Lore",
            description=random.choice(lore_fragments),
            color=discord.Color.dark_red()
        )

        # Set embed footer
        embed.set_footer(text="The Entity whispers in the silence...")
        await interaction.response.send_message(embed=embed)

# This function if required to add the cog to the bot when it's loaded
async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
