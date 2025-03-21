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
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

PREFIXES = [".", "!"]

@app.on_message(filters.command("ban", PREFIXES) & filters.group)
async def ban_user(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("⚠️ **Reply to a user to ban!**")

    target_user = message.reply_to_message.from_user
    chat_id = message.chat.id

    # Check if bot is an admin
    bot_member = await client.get_chat_member(chat_id, client.me.id)
    if not bot_member.status in ["administrator", "creator"]:
        return await message.reply("❌ **I need to be an admin to ban users!**")

    # Check if the user is an admin
    target_member = await client.get_chat_member(chat_id, target_user.id)
    if target_member.status in ["administrator", "creator"]:
        return await message.reply("❌ **I can't ban an admin! Use `.forceban` if you are the owner.**")

    try:
        await client.ban_chat_member(chat_id, target_user.id)
        await message.reply(f"🚫 **Banned {target_user.mention} from the group!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")


@app.on_message(filters.command("forceban", PREFIXES) & filters.group)
async def force_ban_user(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply("❌ **Reply to a user or provide a user ID to force ban!**\nExample: `.forceban 123456789`")

    chat_id = message.chat.id

    # Get user ID from reply or command argument
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.command[1])
        except ValueError:
            return await message.reply("❌ **Invalid user ID!**")

    # Check if bot is the group owner
    bot_member = await client.get_chat_member(chat_id, client.me.id)
    if bot_member.status != "creator":
        return await message.reply("⚠️ **Only the group owner can force-ban admins!**")

    try:
        await client.ban_chat_member(chat_id, user_id)
        await message.reply(f"🚫 **Force-banned `{user_id}` from the group!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")
