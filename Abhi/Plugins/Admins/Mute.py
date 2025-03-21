from pyrogram import filters
from Abhi import app


PREFIXES = [".", "!"] 


@bot.on_message(filters.command("mute", PREFIXES) & filters.group)
async def mute_user(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to mute them!")
    await message.chat.restrict_member(message.reply_to_message.from_user.id, can_send_messages=False)
    await message.reply("User has been muted! 🤐")

@bot.on_message(filters.command("unmute", PREFIXES) & filters.group)
async def unmute_user(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unmute them!")
    await message.chat.restrict_member(message.reply_to_message.from_user.id, can_send_messages=True)
    await message.reply("User has been unmuted! 🔊")
