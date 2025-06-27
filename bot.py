import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.utils import Object
import sqlite3
import os
from flask import Flask
import threading

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
GUILD_ID = 1386301748062453811

class ConfirmView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("✅ ออเดอร์ได้รับการยืนยันแล้ว", ephemeral=True)
        await interaction.user.send("🎉 ออเดอร์ของคุณได้รับการยืนยันแล้ว!")

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.red)
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("❌ ปฏิเสธออเดอร์เรียบร้อย", ephemeral=True)
        await interaction.user.send("❌ ออเดอร์ของคุณถูกปฏิเสธ")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="รายละเอียดออเดอร์")):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, detail TEXT)")
    c.execute("INSERT INTO orders (user, detail) VALUES (?, ?)", (str(interaction.user), รายการ))
    conn.commit()
    conn.close()

    await interaction.response.send_message("📦 ส่งออเดอร์เรียบร้อย รอยืนยันจากแอดมิน", ephemeral=True)

    admin_channel = bot.get_channel(1386302028858523668)  # เปลี่ยนเป็น channel ID จริง
    if admin_channel:
        await admin_channel.send(
            f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:
```{รายการ}```",
            view=ConfirmView()
        )

# Web Admin
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Admin Web พร้อมใช้งาน"

def run_web():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run("MTM4NjMwMTY1MTg4NjkzNjEyNQ.G9mnli.T_-H-ftS4RRrA4uLWqKqX-h7hew-NihlgJhcSk")
