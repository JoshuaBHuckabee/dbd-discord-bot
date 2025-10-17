# cogs/glyphs.py
import discord
from discord.ext import commands

# Define a Cog class to contain the glyph commands of the bot
class Glyphs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def glyph(self, ctx, color: str = None):
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
            "| ⬛     | Black  | Killer   | Deliver stealthily while avoiding survivors     |\n"
            "| ⬜     | White  | Survivor | Interact — causes Blindness & Exhaustion        |\n"
            "| 🟧     | Orange | Survivor | Interact — places fake pallets                  |\n"
            "| 💗     | Pink   | Survivor | Combo — stealth, skill checks, and delivery     |\n"
            "+--------+--------+----------+--------------------------------------------------+\n"
            "```"
        )
        followup = "🔮 Use `!glyph [color]` to summon more knowledge from The Entity *(coming soon).*"
        if color:
            await ctx.send(f"More knowledge about **{color.capitalize()}** glyphs is coming soon.")
        else:
            await ctx.send(glyph_table)
            await ctx.send(followup)

async def setup(bot):
    await bot.add_cog(Glyphs(bot))
