from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from Abhi import app  # Import your bot instance

PREFIXES = [".", "!"]

@app.on_message(filters.command("mute", PREFIXES) & filters.group)
async def mute_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **Reply to a user to mute them!**")

    user_id = message.reply_to_message.from_user.id

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions()  # This removes all permissions, effectively muting the user
        )
        await message.reply(f"🔇 **Muted {message.reply_to_message.from_user.mention} successfully!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

@app.on_message(filters.command("unmute", PREFIXES) & filters.group)
async def unmute_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **Reply to a user to unmute them!**")

    user_id = message.reply_to_message.from_user.id

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True
            )
        )
        await message.reply(f"🔊 **Unmuted {message.reply_to_message.from_user.mention} successfully!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")
        
