from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

PREFIXES = [".", "!"]  # Command prefixes

@app.on_message(filters.command("id", PREFIXES))
async def get_id(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_mention = message.from_user.mention

    # If replied to someone, get their ID too
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        reply_text = (
            f"👤 **Your ID**: `{user_id}`\n"
            f"🏠 **Chat ID**: `{chat_id}`\n"
            f"🔄 **Replied User ID**: `{replied_user.id}`\n"
            f"🔗 **Replied User**: [{replied_user.first_name}](tg://user?id={replied_user.id})"
        )
    else:
        reply_text = (
            f"👤 **Your ID**: `{user_id}`\n"
            f"🏠 **Chat ID**: `{chat_id}`\n"
            f"🔗 **Profile**: [{user_mention}](tg://user?id={user_id})"
        )

    await message.reply(reply_text, disable_web_page_preview=True)
