import discord
from discord.ext import commands
import sqlite3
import os

intents = discord.Intents.default()
intents.message_content = True  # ให้บอทเห็นข้อความ
bot = commands.Bot(command_prefix="/", intents=intents)

DB = "orders.db"

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")

@bot.command()
async def order(ctx, *, text: str):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                 (str(ctx.author.id), text, "รอดำเนินการ", 0))
    conn.commit()
    conn.close()
    await ctx.reply(f"✅ รับออเดอร์แล้ว: `{text}`", mention_author=False)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
