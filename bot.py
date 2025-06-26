import discord
from discord.ext import commands
import sqlite3
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    bot.loop.create_task(notify_confirmed_orders())

@bot.slash_command(name="order", description="ส่งออเดอร์")
async def order(ctx, *, message: str):
    conn = sqlite3.connect("orders.db")
    conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                 (ctx.author.id, message, "รอดำเนินการ", 0))
    conn.commit()
    conn.close()
    await ctx.respond(f"📦 รับออเดอร์แล้ว: `{message}`", ephemeral=True)

async def notify_confirmed_orders():
    await bot.wait_until_ready()
    while True:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id FROM orders WHERE status='ยืนยันแล้ว' AND notified=0")
        rows = cursor.fetchall()
        for order_id, user_id in rows:
            try:
                user = await bot.fetch_user(int(user_id))
                await user.send(f"✅ ออเดอร์ #{order_id} ของคุณได้รับการ *ยืนยัน* แล้วครับ 🎉")
                cursor.execute("UPDATE orders SET notified=1 WHERE id=?", (order_id,))
            except Exception as e:
                print(f"❌ ไม่สามารถส่ง DM ให้ {user_id}: {e}")
        conn.commit()
        conn.close()
        await asyncio.sleep(5)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
