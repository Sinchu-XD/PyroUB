from pyrogram import filters
from pyrogram.types import Message  # ✅ Fix: Import Message
from Abhi import app

PREFIXES = [".", "!"]

# ================= AUTOMATIONS =================
@app.on_message(filters.new_chat_members)
async def welcome_new_members(_, message: Message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Welcome, {user.mention}! Enjoy your stay!")
