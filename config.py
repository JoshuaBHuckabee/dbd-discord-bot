import os
from dotenv import load_dotenv

# Load environment variables from a .env file (e.g., for secrets like bot token)
load_dotenv()

# Retrieve the Discord bot token from the environment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Retrieve channel id from the environment
SACRIFICIAL_TERMINAL_CHANNEL_ID = int(os.getenv("SACRIFICIAL_TERMINAL_CHANNEL_ID"))
OFFERING_TABLE_CHANNEL_ID = int(os.getenv("OFFERING_TABLE_CHANNEL_ID"))
GRIM_NOTEBOOK_CHANNEL_ID = int(os.getenv("GRIM_NOTEBOOK_CHANNEL_ID"))

# List of modules
COGS = [
    "cogs.startup",
    "cogs.news",
    "cogs.core",
    "cogs.glyphs",
    "cogs.events"
]

# Retrieve keyword that denote a patch or upgrade
PATCH_KEYWORDS = [
    "patch", 
    "hotfix", 
    "bugfix", 
    "bug fix", 
    "update", 
    "changelog", 
    "balance", 
    "fixes"
]

# Acceptable glyph colors
GLYPH_COLORS = {
    "red", 
    "blue", 
    "green", 
    "yellow", 
    "purple", 
    "black", 
    "white", 
    "orange", 
    "pink"
    }