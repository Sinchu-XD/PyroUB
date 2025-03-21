from pyrogram import filters
from Abhi import app

PREFIXES = [",", "!"]

@app.on_message(filters.command("ping", PREFIXES))
async def ping(_, message: Message):
    await message.reply("🏓 Pong! Bot is alive.")
