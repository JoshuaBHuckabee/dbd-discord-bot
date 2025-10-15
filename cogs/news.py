import os
import json
import feedparser
from discord.ext import commands, tasks
import discord
from config import OFFERING_TABLE_CHANNEL_ID, GRIM_NOTEBOOK_CHANNEL_ID, PATCH_KEYWORDS

STEAM_FEED_URL = "https://store.steampowered.com/feeds/news/app/381210"
STORED_ITEMS_FILE = "data/steam_news.json"

# Define a Cog class to contain the news commands of the bot
class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_steam_news.start()

    # This method is called when the cog is unloaded from the bot.
    # It cancels the background task so it doesn't keep running in the background
    def cog_unload(self):
        self.check_steam_news.cancel()

    # Fetch the latest Steam news using feed parser
    def fetch_steam_news(self):
        feed = feedparser.parse(STEAM_FEED_URL)
        items = []

        # Loop through each entry
        for entry in feed.entries:
            # Use 'id' to 'link' as a unique identifier
            unique_id = entry.get("id", entry.get("link", ""))

            # Append a simplified dictionary representing the news item
            items.append({
                "id": unique_id,
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "").lower()
            })
        return items

    # Saves the provided list of items to a local JSON file
    def save_items(self, items):
        with open(STORED_ITEMS_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)

    # Loads saved items from the JSON file
    def get_saved_items(self):
        # Check if the file exists before reading it
        if os.path.exists(STORED_ITEMS_FILE):
            with open(STORED_ITEMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    # Determines whether a news items is a patch note
    def is_patch_note(self, item):
        # Combine the title and summary into one string
        text = f"{item['title']} {item.get('summary', '')}".lower()

        # Return True if any patch keyword is found
        return any(keyword in text for keyword in PATCH_KEYWORDS)

    # Sends a Discord embed to a channel with provided news item
    # Adds visual distinction for patch notes using color and description
    async def send_embed(self, channel, item, is_patch=False):
        # Choose embed color based on patch note or not
        color = discord.Color.gold() if is_patch else discord.Color.dark_red()

        # Description label for the embed
        description = "🛠 Patch Note" if is_patch else "Steam News"

        # Create the embed
        embed = discord.Embed(
            title=item["title"],
            url=item["link"],
            description=description,
            color=color
        )

        # Add a footer with the publication date
        embed.set_footer(text=f"Published: {item['published']}")

        # Send the embed
        await channel.send(embed=embed)

    # This task runs automatically every 90 minutes to check for new Steam news items
    @tasks.loop(minutes=90)
    async def check_steam_news(self):
        # Wait until the bot is fully ready before continuing
        await self.bot.wait_until_ready()

        # Retrieve Discord channels by their ID's 
        offering_channel = self.bot.get_channel(OFFERING_TABLE_CHANNEL_ID)
        patch_notes_channel = self.bot.get_channel(GRIM_NOTEBOOK_CHANNEL_ID)

        # If either channel couldn't be found, print an error and exit early
        if not offering_channel or not patch_notes_channel:
            print("One or more channels not found!")
            return

        # Load previously saved Steam news items to avoid reposting duplicates
        saved = self.get_saved_items()
        saved_ids = {item["id"] for item in saved}

        # Fetch the latest news from the Steam API
        fetched = self.fetch_steam_news()

        # Filter out only the new items that haven't been posted before
        new_items = [item for item in fetched if item["id"] not in saved_ids]

        # Separate new items into general news and patch notes
        general_items = [item for item in new_items if not self.is_patch_note(item)]
        patch_items = [item for item in new_items if self.is_patch_note(item)]

        # Log how many new items were found
        #TODO Find a display using rich.py
        print(f"Total new items: {len(new_items)}")
        print(f"Patch notes detected: {len(patch_items)}")
        print(f"General news: {len(general_items)}")

        # Send each general news item to the appropriate Discord channel
        for item in general_items:
            await self.send_embed(offering_channel, item)

        # Send each patch note to the patch notes channel
        for item in patch_items:
            await self.send_embed(patch_notes_channel, item, is_patch=True)

        # Id there were new items, update the saved news list
        if new_items:
            updated = saved + new_items
            updated = updated[-50:]
            self.save_items(updated)

# Standard setup function to register the News cog with the bot
async def setup(bot):
    await bot.add_cog(News(bot))
