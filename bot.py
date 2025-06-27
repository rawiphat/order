import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.utils import get, Object
import sqlite3
import os

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1386301748062453811

class ConfirmView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("ออเดอร์ได้รับการยืนยันแล้ว", ephemeral=True)

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.red)
    async def deny(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("ออเดอร์ถูกปฏิเสธ", ephemeral=True)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Sync failed: {e}")
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="พิมพ์รายการที่ต้องการ")):
    # insert to SQLite
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, content TEXT)")
    c.execute("INSERT INTO orders (user, content) VALUES (?, ?)", (str(interaction.user), รายการ))
    conn.commit()
    conn.close()

    # ส่งไปยัง Admin Channel
    admin_channel = bot.get_channel(YOUR_ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(
            f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:
```{รายการ}```",
            view=ConfirmView()
        )
    await interaction.user.send("📦 ออเดอร์ของคุณถูกส่งไปยังแอดมินแล้ว")
    await interaction.response.send_message("✅ ส่งออเดอร์เรียบร้อย", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
