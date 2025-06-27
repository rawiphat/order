import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.utils import Object
from flask import Flask, render_template
import sqlite3
import threading
import os

TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_TOKEN_HERE"
GUILD_ID = 1386301748062453811
ADMIN_CHANNEL_ID = 1386302028858523668  # <- ใส่ channel id จริงตรงนี้

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        username TEXT,
        order_text TEXT,
        status TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

class ConfirmView(nextcord.ui.View):
    def __init__(self, order_id, user_id):
        super().__init__(timeout=None)
        self.order_id = order_id
        self.user_id = user_id

    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.success)
    async def confirm(self, button: nextcord.ui.Button, interaction: Interaction):
        self.update_status("confirmed")
        await interaction.response.send_message("✅ ออเดอร์ได้รับการยืนยันแล้ว", ephemeral=True)
        await self.notify_user("ออเดอร์ของคุณได้รับการ *ยืนยัน* แล้ว ✅")

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.danger)
    async def reject(self, button: nextcord.ui.Button, interaction: Interaction):
        self.update_status("rejected")
        await interaction.response.send_message("❌ ออเดอร์ถูกปฏิเสธแล้ว", ephemeral=True)
        await self.notify_user("ออเดอร์ของคุณถูก *ปฏิเสธ* ❌")

    def update_status(self, status):
        conn = sqlite3.connect("orders.db")
        c = conn.cursor()
        c.execute("UPDATE orders SET status=? WHERE id=?", (status, self.order_id))
        conn.commit()
        conn.close()

    async def notify_user(self, message):
        user = await bot.fetch_user(self.user_id)
        if user:
            await user.send(message)

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="รายละเอียดออเดอร์")):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, username, order_text, status) VALUES (?, ?, ?, ?)", (
        str(interaction.user.id), interaction.user.name, รายการ, "pending"))
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(
    f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:\n```{รายการ}```",
    view=ConfirmView(order_id, interaction.user.id)
)

    await interaction.response.send_message("📬 ส่งออเดอร์เรียบร้อยแล้ว รอการยืนยัน", ephemeral=True)

@app.route("/")
def index():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT id, user_id, username, order_text, status FROM orders ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", orders=rows)

def run_web():
    init_db()
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run(TOKEN)
