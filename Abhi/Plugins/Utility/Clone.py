from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

@app.on_message(filters.command("clone", [".", "!"]) & filters.private)
async def clone_profile(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("Reply to a user to clone their profile!")

    target_user = message.reply_to_message.from_user

    # Clone Name
    if target_user.first_name:
        await client.update_profile(first_name=target_user.first_name, last_name=target_user.last_name)

    # Clone Username
    if target_user.username:
        await client.set_username(target_user.username)  # Fixed this line

    # Clone Profile Picture
    photos = await client.get_profile_photos(target_user.id)
    if photos:
        photo_path = await client.download_media(photos[0].file_id)
        await client.set_profile_photo(photo=photo_path)

    await message.reply(f"Successfully cloned {target_user.mention}!")



@app.on_message(filters.command("unclone", PREFIXES) & filters.private)
async def unclone(client, message):
    global original_profile

    if not original_profile:
        return await message.reply("❌ **No original profile saved!**")

    await client.update_profile(
        first_name=original_profile["name"],
        bio=original_profile["bio"]
    )

    await client.delete_profile_photos()
    await message.reply("🔄 **Profile restored to original settings!**")
