from pyrogram import filters
from Abhi import app



# ================= AUTOMATIONS =================
@app.on_message(filters.new_chat_members)
async def welcome_new_members(_, message: Message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Welcome, {user.mention}! Enjoy your stay!")
