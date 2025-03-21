from pyrogram import filters
from pyrogram.types import Message  # ✅ Fix: Import Message
from Abhi import app


PREFIXES = [".", "!"]

@app.on_message(filters.command("id", PREFIXES))
async def get_id(_, message: Message):
    await message.reply(f"👤 Your ID: `{message.from_user.id}`\n🏠 Chat ID: `{message.chat.id}`")
  
