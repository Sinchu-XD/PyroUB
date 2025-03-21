from pyrogram import filters
from pyrogram.types import Message  # ✅ Fix: Import Message
from Abhi import app


PREFIXES = [".", "!"]

# Unban Member In Group
@app.on_message(filters.command("unban", PREFIXES) & filters.group)
async def unban(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unban them.")
    user_id = message.reply_to_message.from_user.id
    await client.unban_chat_member(message.chat.id, user_id)
    await message.reply(f"Successfully unbanned {user_id}.")


# Ban Member In Group 
@app.on_message(filters.command("ban", PREFIXES) & filters.group)
async def ban_user(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to ban them!")
    await message.chat.ban_member(message.reply_to_message.from_user.id)
    await message.reply("User has been banned! ✅")
