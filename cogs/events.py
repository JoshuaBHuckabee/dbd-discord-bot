import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import json
import os

EVENTS_FILE = "data/events.json"

# Define a Cog class to contain the event commands of the bot
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load events from JSON file
    def load_events(self):
        if not os.path.exists(EVENTS_FILE):
            return []
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Define a slash command: /events
    # Displays the list of upcoming events in an embed
    @app_commands.command(name="events", description="Upcoming events!")
    async def events(self, interaction: discord.Interaction):
        events = self.load_events()

        # Get current UTC time (timezone-aware)
        now = datetime.now(timezone.utc)

        upcoming = []
        for ev in events:
            try:
                # Parse strings and ensure they're timezone-aware
                start = datetime.fromisoformat(ev["start"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(ev["end"].replace("Z", "+00:00"))

                # Only show events that haven't ended yet
                if end > now:
                    upcoming.append((start, end, ev))
            except Exception:
                continue  # Skip invalid event entries silently

        if not upcoming:
            await interaction.response.send_message("☁️ The Fog reveals no upcoming trials...")
            return

        # Sort events by start time
        upcoming.sort(key=lambda e: e[0])

        # Create the embed
        embed = discord.Embed(
            title="📅 Upcoming Events",
            description="The Entity has marked these trials...",
            color=discord.Color.dark_red(),
            timestamp=datetime.now(timezone.utc)  # Use timezone-aware datetime
        )

        embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Add each upcoming event to the embed
        for start, end, ev in upcoming[:5]:  # Show up to 5 events
            name = ev["name"]
            desc = ev.get("description", "")
            start_str = start.strftime("%b %d, %Y")
            end_str = end.strftime("%b %d, %Y")
            embed.add_field(
                name=f"🩸 {name}",
                value=f"{desc}\n**Start:** {start_str} | **End:** {end_str}",
                inline=False
            )
            embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Set embed footer
        embed.set_footer(text="The trials await...")
        await interaction.response.send_message(embed=embed)

# Register this cog with the bot
async def setup(bot):
    await bot.add_cog(Events(bot))
