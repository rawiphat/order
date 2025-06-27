import nextcord
from nextcord import Interaction, SlashOption, Object
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1386301748062453811
ADMIN_CHANNEL_ID = 1386302028858523668

intents = nextcord.Intents.default()
intents.message_content = True

bot = nextcord.Bot(intents=intents)

class ConfirmView(nextcord.ui.View):
    @nextcord.ui.button(label="✅ ยืนยัน", style=nextcord.ButtonStyle.success)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("ออเดอร์ได้รับการยืนยันแล้ว ✅", ephemeral=True)

    @nextcord.ui.button(label="❌ ปฏิเสธ", style=nextcord.ButtonStyle.danger)
    async def reject(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("ออเดอร์ถูกปฏิเสธ ❌", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=Object(id=GUILD_ID))
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="order", description="ส่งออเดอร์", guild=Object(id=GUILD_ID))
async def order(interaction: Interaction, รายการ: str = SlashOption(description="พิมพ์รายการ")):
    await interaction.response.send_message("📤 ส่งออเดอร์แล้ว รอยืนยัน...", ephemeral=True)
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(
            f"📥 มีออเดอร์ใหม่จาก {interaction.user.mention}:"
```{รายการ}```",
            view=ConfirmView()
        )

bot.run(TOKEN)
