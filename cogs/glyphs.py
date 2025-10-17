import discord
from discord.ext import commands
from discord import app_commands
from config import GLYPH_COLORS

# Define a Cog class to contain the glyph commands of the bot
class Glyphs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define a slash command: /glyph
    # Displays a table of all the glyphs, roles, and objectives to complete.
    @app_commands.command(name="glyph", description="Glyph Guide Table")
    @app_commands.describe(color="Optional color of the glyph you want info about")
    async def glyph(self, interaction: discord.Interaction, color: str = None):
        
        if color:
            color_lower = color.lower()
            if color_lower not in self.GLYPH_COLORS:
                return await interaction.response.send_message(
                    f"'{color}' is not a valid glyph color. Choose from: {', '.join(sorted(self.GLYPH_COLORS))}.",
                    ephemeral=True
                )
            # Placeholder: detailed info soon
            return await interaction.response.send_message(
                f"More knowledge about **{color_lower.capitalize()}** glyphs is coming soon."
            )
            
        # If no color, send the full table + hint in one message
        glyph_table = (
            "```text\n"
            "+--------+--------+----------+--------------------------------------------------+\n"
            "| Glyph  | Color  | Role     | Objective                                        |\n"
            "+--------+--------+----------+--------------------------------------------------+\n"
            "| 🟥     | Red    | Survivor | Interact — appears randomly in the trial        |\n"
            "| 🟦     | Blue   | Survivor | Hit skill checks while chased                   |\n"
            "| 🟩     | Green  | Survivor | Carry to location — avoid killer                |\n"
            "| 🟨     | Yellow | Survivor | Follows you — makes noise, hard to hide         |\n"
            "| 🟪     | Purple | Killer   | Interact — gain Hindered & Blindness effects    |\n"
            "| ⚫     | Black  | Killer   | Deliver stealthily while avoiding survivors     |\n"
            "| ⚪     | White  | Survivor | Interact — causes Blindness & Exhaustion        |\n"
            "| 🟧     | Orange | Survivor | Interact — places fake pallets                  |\n"
            "| 💗     | Pink   | Survivor | Combo — stealth, skill checks, and delivery     |\n"
            "+--------+--------+----------+--------------------------------------------------+\n"
            "```"
        )
        followup = "🔮 Use `!glyph [color]` to summon more knowledge from The Entity *(coming soon).*"
        
        # Use a single combined message
        await interaction.response.send_message(f"{glyph_table}\n{followup}")

async def setup(bot):
    await bot.add_cog(Glyphs(bot))
