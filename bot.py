import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import sqlite3
import os

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

DB = "orders.db"

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print("❌ Sync failed:", e)
    print(f"🤖 Logged in as {bot.user}")

@bot.slash_command(name="order", description="ส่งออเดอร์ใหม่")
async def order(interaction: Interaction,
                text: str = SlashOption(description="ข้อความออเดอร์")):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                 (str(interaction.user.id), text, "รอดำเนินการ", 0))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ รับออเดอร์แล้ว: `{text}`", ephemeral=True)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
