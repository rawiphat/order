import nextcord as discord
from nextcord.ext import commands
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")

@bot.slash_command(name="order", description="ส่งออเดอร์")
async def order(ctx, *, text: str):
    conn = sqlite3.connect("orders.db")
    conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                 (str(ctx.author.id), text, "รอดำเนินการ", 0))
    conn.commit()
    conn.close()
    await ctx.respond("✅ รับออเดอร์แล้ว", ephemeral=True)

bot.run("YOUR_DISCORD_BOT_TOKEN")
