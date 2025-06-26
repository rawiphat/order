import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import os

intents = discord.Intents.default()
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

@bot.tree.command(name="order", description="ส่งออเดอร์ใหม่")
@app_commands.describe(text="ข้อความออเดอร์")
async def order(interaction: discord.Interaction, text: str):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                 (str(interaction.user.id), text, "รอดำเนินการ", 0))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ รับออเดอร์แล้ว: `{text}`", ephemeral=True)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
