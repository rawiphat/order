import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Object

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1386301748062453811  # เปลี่ยนเป็น Guild ID ของคุณ
ADMIN_CHANNEL_ID = 123456789012345678  # เปลี่ยนเป็น Channel ID ของแอดมิน

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

class ConfirmView(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.success)
    async def confirm(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("✅ ยืนยันออเดอร์แล้ว", ephemeral=True)
        user = await bot.fetch_user(self.user_id)
        if user:
            await user.send("✅ ออเดอร์ของคุณได้รับการยืนยันแล้ว")

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.danger)
    async def reject(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("❌ ปฏิเสธออเดอร์แล้ว", ephemeral=True)
        user = await bot.fetch_user(self.user_id)
        if user:
            await user.send("❌ ออเดอร์ของคุณถูกปฏิเสธ")

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="รายละเอียด")):
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(
            f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:
```{รายการ}```",
            view=ConfirmView(interaction.user.id)
        )
    await interaction.response.send_message("📬 ส่งออเดอร์เรียบร้อยแล้ว", ephemeral=True)

bot.run(TOKEN)