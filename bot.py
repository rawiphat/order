import os
from ext.commands import Bot

bot = Bot(command_prefix="/")

@bot.event
def on_ready():
    print("✅ Bot is online and ready!")

@bot.command()
def ping():
    print("🏓 Pong!")

@bot.slash_command(name="order", description="สั่งออเดอร์")
def order():
    print("🛒 รับออเดอร์แล้ว")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN", "dummy-token"))