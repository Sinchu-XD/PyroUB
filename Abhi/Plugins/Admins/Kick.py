from pyrogram import filters
from Abhi import app

PREFIXES = [".", "!"]


# 👢 Kick User (Bans & Unbans Immediately)
@app.on_message(filters.command("kick", PREFIXES) & filters.group)
async def kick_user(client, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply to a user to kick them!**")
    
    user_id = message.reply_to_message.from_user.id

    try:
        await client.ban_chat_member(message.chat.id, user_id)  # Ban the user
        await client.unban_chat_member(message.chat.id, user_id)  # Unban immediately (kick effect)

        await message.reply(f"👢 **User Kicked!**\n🚪 {message.reply_to_message.from_user.mention} **has been removed from the group!**")
    except Exception as e:
        await message.reply(f"❌ **Failed to kick user!**\n**Error:** `{str(e)}`")
