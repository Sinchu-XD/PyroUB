import json
import os
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UsernameOccupied, RPCError
from Abhi import app  # Import your bot instance

PREFIXES = [".", "!"]
PROFILE_BACKUP_FILE = "profile_backup.json"  # File to save the original profile


def save_profile_to_file(profile_data):
    """ Save profile backup to a JSON file """
    with open(PROFILE_BACKUP_FILE, "w") as file:
        json.dump(profile_data, file)


def load_profile_from_file():
    """ Load profile backup from a JSON file """
    if os.path.exists(PROFILE_BACKUP_FILE):
        with open(PROFILE_BACKUP_FILE, "r") as file:
            return json.load(file)
    return None


@app.on_message(filters.command("clone", PREFIXES) & filters.private)
async def clone_profile(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("⚠️ **Reply to a user to clone their profile!**")

    target_user = message.reply_to_message.from_user

    # Save Original Profile Before Cloning
    me = await client.get_me()
    chat_info = await client.get_chat(me.id)  # Fetch chat details
    original_photos = [photo async for photo in client.get_chat_photos(me.id)]

    original_profile = {
        "name": me.first_name,
        "last_name": me.last_name,
        "bio": chat_info.bio if hasattr(chat_info, "bio") else "",
        "photos": [photo.file_id for photo in original_photos]
    }
    save_profile_to_file(original_profile)  # Save to file

    try:
        # Clone Name
        if target_user.first_name:
            await client.update_profile(
                first_name=target_user.first_name,
                last_name=target_user.last_name
            )

        # Clone Username
        if target_user.username:
            new_username = target_user.username + "_clone"
            try:
                await client.set_username(new_username)
            except UsernameOccupied:
                new_username = target_user.username + "_xx"
                await client.set_username(new_username)

        # Clone Bio
        target_chat_info = await client.get_chat(target_user.id)
        target_bio = target_chat_info.bio if hasattr(target_chat_info, "bio") else None
        if target_bio:
            await client.update_profile(bio=target_bio)

        # Clone Profile Picture
        target_photos = [photo async for photo in client.get_chat_photos(target_user.id)]
        if target_photos:
            photo_path = await client.download_media(target_photos[0].file_id)
            await client.set_profile_photo(photo=photo_path)

        await message.reply(
            f"✅ **Successfully cloned:** {target_user.mention}\n\n"
            "✨ **Cloned Data:**\n"
            "🔹 Name\n"
            "🔹 Username\n"
            "🔹 Bio\n"
            "🔹 Profile Picture"
        )

    except RPCError as e:
        await message.reply(f"❌ **Telegram Error:** `{e}`")

    except Exception as e:
        await message.reply(f"⚠️ **Unexpected Error:** `{e}`")


@app.on_message(filters.command("unclone", PREFIXES) & filters.private)
async def unclone(client, message: Message):
    original_profile = load_profile_from_file()  # Load saved profile

    if not original_profile:
        return await message.reply("⚠️ **No original profile saved!**")

    try:
        # Restore Original Profile
        await client.update_profile(
            first_name=original_profile["name"],
            last_name=original_profile.get("last_name", ""),
            bio=original_profile["bio"]
        )

        # Restore Original Profile Picture
        if original_profile["photos"]:
            photo_path = await client.download_media(original_profile["photos"][0])
            await client.set_profile_photo(photo=photo_path)
        else:
            await client.delete_profile_photos()

        await message.reply("🔄 **Profile restored to original settings!**")

        # Delete backup after restoring
        os.remove(PROFILE_BACKUP_FILE)

    except Exception as e:
        await message.reply(f"⚠️ **Error restoring profile:** `{e}`")
                
