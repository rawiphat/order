
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
from nextcord.utils import Object
import sqlite3
import os

TOKEN = os.getenv("DISCORD_TOKEN") or "MTM4NjMwMTY1MTg4NjkzNjEyNQ.G9mnli.T_-H-ftS4RRrA4uLWqKqX-h7hew-NihlgJhcSk"
GUILD_ID = 1386301748062453811

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

class ConfirmView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("ออเดอร์ของคุณได้รับการยืนยันแล้วใน DM!", ephemeral=True)
        await interaction.user.send("✅ ออเดอร์ของคุณได้รับการยืนยันแล้ว ขอบคุณค่ะ!")

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.red)
    async def deny(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("ออเดอร์ของคุณถูกปฏิเสธแล้ว", ephemeral=True)
        await interaction.user.send("❌ ขออภัย ออเดอร์ของคุณถูกปฏิเสธ")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.slash_command(name="order", description="ส่งออเดอร์", guild_ids=[GUILD_ID])
async def order_command(interaction: Interaction, รายการ: str):
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(
            f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:\n```{รายการ}```",
            view=ConfirmView()
        )
    await interaction.response.send_message("✅ ส่งออเดอร์เรียบร้อยแล้ว!", ephemeral=True)

bot.run(TOKEN)
