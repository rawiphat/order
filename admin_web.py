from flask import Flask
import threading
import asyncio
import nextcord
from nextcord.ext import commands
import os

TOKEN = "MTM4NjMwMTY1MTg4NjkzNjEyNQ.G9mnli.T_-H-ftS4RRrA4uLWqKqX-h7hew-NihlgJhcSk"
GUILD_ID = 1386301748062453811

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Admin Web Running"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

def run_bot():
    asyncio.run(bot.start(TOKEN))

if __name__ == "__main__":
    # 🔁 เรียก bot
    threading.Thread(target=run_bot).start()

    # 🌐 รัน Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
