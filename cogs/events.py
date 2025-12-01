import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import json
import os
import aiohttp, asyncio

# URL of render-hosted API endpoint
API_URL = "https://dbd-news-api.onrender.com/api/news"

# Define a Cog class to contain the event commands of the bot
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load events from API source
    async def get_events(self):
        """
        Fetch events from the API asynchronously using aiohttp.
        Only keeps items where contentType === "event".
        Handles timeouts and connection errors gracefully
        """
        try: 
            # Create am async HTTP session
            async with aiohttp.ClientSession() as session:

                # Make GET request with 10-second timeout
                async with session.get(API_URL, timeout=10) as response:

                    # Raises exception if status is not 200
                    response.raise_for_status()

                    # Convert the JSON response into a Python list/dict
                    data = await response.json()
        
                    # Filter: keep only the items where contentType == "event"
                    events = [item for item in data if item.get("contentType") == "event"]

                    # Return only those filtered event items
                    return events

        # Triggered if API doesn't respond in time
        except asyncio.TimeoutError:
            print("API request timed out")
            return []

        # Triggered if DNS fails, no internet, or API is down
        except aiohttp.ClientError as e:
            print(f"API connection error: {e}")
            return []          
        
    # Load codes from API source
    async def get_codes(self):
        """
        Fetch codes from the API asynchronously using aiohttp.
        Only keeps items where contentType === "code".
        Handles timeouts and connection errors gracefully
        """

        try: 
            # Create am async HTTP session
            async with aiohttp.ClientSession() as session:

                # Make GET request with 10-second timeout
                async with session.get(API_URL, timeout=10) as response:

                    # Raises exception if status is not 200
                    response.raise_for_status()

                    # Convert the JSON response into a Python list/dict
                    data = await response.json()
        
                    # Filter: keep only the items where contentType == "event"
                    codes = [item for item in data if item.get("contentType") == "code" and item.get("code")]

                    # Return only those filtered event items
                    return codes

        # Triggered if API doesn't respond in time
        except asyncio.TimeoutError:
            print("API request timed out")
            return []

        # Triggered if DNS fails, no internet, or API is down
        except aiohttp.ClientError as e:
            print(f"API connection error: {e}")
            return []          

    # Define a slash command: /events
    # Displays the list of upcoming events in an embed
    @app_commands.command(name="events", description="Upcoming events!")
    async def events(self, interaction: discord.Interaction):
        """
        Displays a list of upcoming events using the dbd API.
        Fully async-friendly.
        """

        # Tell Discord we are thinking
        await interaction.response.defer()
        
        # Fetch events from the API
        events = await self.get_events()

        # If the API returned no events, show a friendly message
        if not events:
            await interaction.followup.send("☁️ The Fog reveals no upcoming trials...")
            return

        # Sort by 'publishedAt' so the oldest events appear first
        events.sort(key=lambda e: e.get("publishedAt"))

        # Create the embed
        embed = discord.Embed(
            title="📅 Upcoming Events",
            description="The Entity has marked these trials...",
            color=discord.Color.dark_red(),
            timestamp=datetime.now(timezone.utc)  # current UTC time
        )

        # Spacer for visual clarity
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Set a general icon (optional)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/4b/IconCurrency_bloodpoints.png/revision/latest?cb=20180702212847")  # Bloodpoints logo

        # Add each event to the embed
        for ev in events[:5]: # Show up to 5 events
            # Extract fields from the API response
            title = ev.get("title", "Untitled Event")
            content = ev.get("content", "No description provided.")
            url = ev.get("url")

            # Build the field text
            value_text = content
            if url:
                value_text += f"\n[🔗 More Info]({url})" # Markdown clickable link
            
            # Add the event as a field
            embed.add_field(name=f"🩸 {title}\n", value=value_text, inline=False)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # spacer

        # Set embed footer
        embed.set_footer(text="The trials await...")
        await interaction.followup.send(embed=embed)

    # Define a slash command: /codes
    # Displays active redeemable codes
    @app_commands.command(name="codes", description="Redeemable Dead by Daylight Codes!")
    async def codes(self, interaction: discord.Interaction):

        await interaction.response.defer()

        # Fetch list of codes
        codes = await self.get_codes()

        if not codes:
            return await interaction.followup.send("☁️ The Fog reveals no redeemable codes at this time...")

        # Sort codes by published date (newest first)
        codes.sort(key=lambda e: e.get("publishedAt"), reverse=True)

        # Create embed
        embed = discord.Embed(
            title="💀 Active Redeemable Codes",
            description="These offerings have been revealed by The Entity:",
            color=discord.Color.dark_red(),
            timestamp=datetime.now(timezone.utc)
        )

        # Set a general icon (optional)
        embed.set_thumbnail(url="https://toppng.com/uploads/preview/dead-by-daylight-white-logo-type-design-11733954264hlxoyqh0ou.webp")  # Example DBD icon (replace if needed)

        # Loop through codes and add entries
        for ev in codes[:5]:  # show up to 5 entries
            content = ev.get("content", "No description available.")
            code = ev.get("code", "Unknown")
            url = ev.get("url")

            # Build field value
            value_text = (
                f"**🎟️ Code: `{code}` 🎟️**\n"
                f"{content}*\n"
            )

            if url:
                value_text += f"[🔗 Source]({url})"

            # Add the text as a field
            embed.add_field(name="\u200b", value=value_text, inline=False)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # spacer

        embed.set_footer(text="Enter these codes in the in-game Store.")
        await interaction.followup.send(embed=embed)



# Register this cog with the bot
async def setup(bot):
    await bot.add_cog(Events(bot))
