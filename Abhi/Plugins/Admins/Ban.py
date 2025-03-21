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


from pyrogram import filters
from pyrogram.types import ChatPrivileges, Message
from Abhi import app

PREFIXES = [".", "!"]

@app.on_message(filters.command("ban", PREFIXES) & filters.group)
async def ban_user(client, message: Message):
    if not message.from_user:
        return await message.reply("❌ **I can't verify your identity!**")

    chat_id = message.chat.id
    user_id = message.from_user.id
    bot_self = await client.get_chat_member(chat_id, "me")  # Get bot info
    user_self = await client.get_chat_member(chat_id, user_id)

    # Check if the bot is an admin
    if not bot_self.privileges or not bot_self.privileges.can_restrict_members:
        return await message.reply("❌ **I need to be an admin to ban users!**")

    # Check if the user has permission to ban
    if not user_self.privileges or not user_self.privileges.can_restrict_members:
        return await message.reply("❌ **You don't have permission to ban users!**")

    # Ensure a user is replied to
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("⚠️ **Reply to a user to ban them!**")

    target_user = message.reply_to_message.from_user

    # Prevent banning another admin unless using ForceBan
    target_info = await client.get_chat_member(chat_id, target_user.id)
    if target_info.privileges and not message.command[0] == "forceban":
        return await message.reply("⚠️ **You can't ban an admin! Use `.forceban` if necessary.**")

    try:
        await client.ban_chat_member(chat_id, target_user.id)
        await message.reply(f"✅ **{target_user.mention} has been banned!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")


@app.on_message(filters.command("forceban", PREFIXES) & filters.group)
async def force_ban_user(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("⚠️ **Reply to a user to force ban them!**")

    chat_id = message.chat.id
    target_user = message.reply_to_message.from_user

    bot_self = await client.get_chat_member(chat_id, "me")

    if not bot_self.privileges or not bot_self.privileges.can_restrict_members:
        return await message.reply("❌ **I need to be an admin to ban users!**")

    try:
        await client.ban_chat_member(chat_id, target_user.id)
        await message.reply(f"🚨 **{target_user.mention} has been force-banned!** 🚫")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

