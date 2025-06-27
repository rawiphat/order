import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.utils import Object
from flask import Flask, render_template
import sqlite3, threading, os

TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_TOKEN_HERE"
GUILD_ID = 1386301748062453811

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, username TEXT,
        order_text TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, user_id, username, order_text, status FROM orders ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", orders=rows)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="รายการ")):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, username, order_text, status) VALUES (?, ?, ?, ?)",
              (str(interaction.user.id), interaction.user.name, รายการ, "pending"))
    conn.commit()
    conn.close()
    await interaction.response.send_message("📬 ออเดอร์ของคุณถูกส่งแล้ว", ephemeral=True)

def run_web():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run(TOKEN)