# DBD Discord Bot

A custom-built Discord bot for managing **Dead by Daylight** content, including event tracking, glyphs, news updates, and more.

---

# Bot Features & Architecture

## Core Features

### Event Management
- Loads and displays upcoming Dead by Daylight events from a self-curated `events.json`.
- Ideal for community calendars or in-server event alerts.

### Steam News Integration
- Fetches official Dead by Daylight news from Steam.
- Automatically separates news into:
  - Patch Notes
  - General Updates
- Posts news to appropriate channels (e.g., patch notes channel vs. news channel).

---

## Architecture & Design

### Modular Cog-Based System
- Built using Discord.py’s cog system.
- Enables clean separation of functionality.
- Scalable and maintainable by adding or removing cogs as needed.

### Slash Command Support
- Full support for Discord's modern slash commands (`/command`).
- Commands include built-in descriptions and clean UI integration.

---

## Developer-Friendly

### Easily Extensible
- Drop in custom cogs to expand bot functionality.
- Add your own commands and background tasks.
- Clean API for command registration and bot setup.

---

## Summary

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

```python
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install Dependencies

```python
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file at the project root:

```bash
DISCORD_TOKEN=your-bot-token-here
CHANNEL_NAME=your-channel-name-here
```

### 5. Run the bot

```bash
python main.py
```

## 📁 Setup Instructions

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
