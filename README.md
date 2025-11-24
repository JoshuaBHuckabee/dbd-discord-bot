# DBD Discord Bot

[![Discord](https://img.shields.io/discord/1296581187112013904.svg?label=Discord&logo=discord&color=7289da)](https://discord.gg/3JrzDaB2)  
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg?label=Python&logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/github/license/JoshuaBHuckabee/dbd-discord-bot.svg?label=License)](LICENSE)  

A custom-built Discord bot for managing **Dead by Daylight** content, including event tracking, glyph guide, news and patch updates, and more.

---

## Table of Contents

- [DBD Discord Bot](#dbd-discord-bot)
  - [Table of Contents](#table-of-contents)
- [Project Update](#project-update)
  - [New Direction: Aggregator API](#new-direction-aggregator-api)
    - [Core Features](#core-features)
  - [Tech Stack](#tech-stack)
  - [Integration Path](#integration-path)
  - [Bot Features \& Architecture](#bot-features--architecture)
    - [Core Features](#core-features-1)
      - [Event Management](#event-management)
      - [Steam News Integration](#steam-news-integration)
    - [Architecture \& Design](#architecture--design)
      - [Modular Cog-Based System](#modular-cog-based-system)
      - [Slash Command Support](#slash-command-support)
    - [Developer-Friendly](#developer-friendly)
      - [Easily Extensible](#easily-extensible)
    - [Summary](#summary)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create and Activate the Virtual Environment](#2-create-and-activate-the-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Set Up Environment Variables](#4-set-up-environment-variables)
    - [5. Run the bot](#5-run-the-bot)
  - [Project Structure](#project-structure)
  - [Usage Examples](#usage-examples)
    - [Slash Commands](#slash-commands)
  - [Extending the Bot](#extending-the-bot)
  - [Contributing \& License](#contributing--license)

---
# Project Update

The bot now features **API-driven event display**, fetching upcoming Dead by Daylight events from the dbd-news-api. This ensures communities always see the latest events without relying on a local events.json file.

**News and patch notes continue to be fetched and posted using the existing Steam/news integration**, ensuring communities still receive official updates in real time.

The project is gradually moving toward a modular **aggregator API**, centralizing all DBD news and updates across platforms:

→ https://github.com/JoshuaBHuckabee/dbd-news-api

---

## New Direction: Aggregator API

This new API will eventually take over the bot’s event and news features, providing a single source of truth for *Dead by Daylight* content.

### Core Features
- **Multi-Platform Scraping** — Collects news and updates from official sources including:
  - YouTube  
  - Steam  
  - The Dead by Daylight official website
- **Structured Storage** — Saves all fetched data into a **Neon PostgreSQL** database using **Prisma ORM**.
- **Clean & Queryable API** — Provides endpoints to fetch, filter, and paginate news items for any client or bot.
- **Manual Control** — Scrapers can be run on demand — no automatic background fetching.
- **Duplicate Protection** — Ensures unique entries using URL-based deduplication.
- **Extensible Design** — Easily add new platforms (e.g. Reddit, Instagram, Twitter/X) with minimal setup.

---

## Tech Stack
- **Node.js + Express** — Backend & API framework  
- **Prisma ORM + Neon PostgreSQL** — Database and schema management  
- **Axios, Cheerio, fast-xml-parser** — Web scraping utilities  
- **dotenv** — Environment configuration

---

## Integration Path
Once stable, the Aggregator API will serve as the **backend foundation** for the existing Discord bot — powering event listings, patch notes, and official updates directly from the unified data source.

---

## Bot Features & Architecture

### Core Features

#### Event Management
- Fetches events from `dbd-news-api` for a centralized and always-current source.
- Each event is shown using **rich embeds**, including fields like title, description, platform, and link.
- Includes error handling for missing or malformed data from the API.
- The bot does not perform **sorting, filtering, or date calculations** — all event logic is handled by the scripts that populate the API.
- **Manual reminders**: users or admins can trigger notifications for events in Discord channels.
- Does not rely on local JSON files or event dates; sorting/filtering is based on available metadata.

Removes dependency on local events.json, streamlining event updates and ensuring accuracy.  
- ~~Loads and displays upcoming Dead by Daylight events from a self‑curated `events.json`.~~
- ~~Ideal for community calendars or in-server event alerts.~~

#### Steam News Integration  
- Fetches official DBD news from Steam.  
- Automatically separates news into:
  - Patch Notes  
  - General Updates  
- Posts news to appropriate channels (e.g. patch notes channel vs. news channel).

---

### Architecture & Design

#### Modular Cog-Based System  
- Built using Discord.py’s cog system.  
- Enables clean separation of functionality.  
- Scalable and maintainable: add or remove cogs as needed.

#### Slash Command Support  
- Full support for Discord’s modern slash commands (`/command`).  
- Commands include built-in descriptions and clean UI integration.

---

### Developer-Friendly

#### Easily Extensible  
- Drop in custom cogs to expand functionality.  
- Add your own commands and background tasks.  
- Clean API for command registration and bot setup.

---

### Summary

A scalable, feature-rich Discord bot for Dead by Daylight communities —  
blending automated event tracking, real-time news integration, and an extensible architecture built for long-term support.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/dbd-discord-bot.git
cd dbd-discord-bot
```

### 2. Create and Activate the Virtual Environment

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```python
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file at the project root:

```bash
DISCORD_TOKEN=your-bot-token-here
NEWS_CHANNEL_ID=1234567890
PATCH_NOTES_CHANNEL_ID=9876543210
# Add any other config variables you need
```

### 5. Run the bot

```bash
python main.py
```

## Project Structure

<pre>
dbd_bot/
│
├── bot.py             # Bot creation and cog loading
├── main.py            # Starts and runs the bot
├── config.py          # Loads environment and settings
├── .env               # Bot token (not tracked in Git)
│
├── cogs/              # Modular features
│   ├── core.py
│   ├── events.py
│   └── ...
│
├── data/              # JSON data files (events, steam news)
│   ├── events.json
│   └── steam_news.json
│
├── assets/            # Images, emojis, etc.
│
├── requirements.txt
├── .gitignore
└── README.md
</pre>

---

## Usage Examples

### Slash Commands

- `/ping` — Test if the bot is online.
- `/players` — Show current active players on Steam.
- `/lore` — Get a random lore fragment about The Entity.
- `/glyph` — Display a table of glyph objectives. (/command coming soon!)
- `/events` — List upcoming DBD community events.

---

## Extending the Bot

To add your own functionality:
   1. Create a new cog file under cogs/, e.g. my_cog.py.
   2. Define a class inheriting from commands.Cog, register commands / tasks.
   3. Use the boilerplate:

```python
from discord.ext import commands
from discord import app_commands  # if you want slash commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction):
        await interaction.response.send_message("Hello, from MyCog!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

   4. The bot will automatically load it if your bot.py / main.py scans cogs/.

---

## Contributing & License

Contributions, feedback, and issues are welcome!
Feel free to open PRs or feature requests.
