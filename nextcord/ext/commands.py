
import os
from nextcord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = commands.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
