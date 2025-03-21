import os
from pyrogram import Client, filters
from Abhi import app

PREFIXES = [".", "!"]

@app.on_message(filters.command("clone", PREFIXES) & filters.private)
async def clone_profile(client, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply to a user's message to clone their profile!**")

    target_user = message.reply_to_message.from_user

    # ✅ Clone Name
    if target_user.first_name:
        new_name = target_user.first_name
        if target_user.last_name:
            new_name += f" {target_user.last_name}"
        await client.update_profile(first_name=new_name)
    
    # ✅ Clone Username (if exists)
    if target_user.username:
        await client.update_username(target_user.username)

    # ✅ Clone Bio (About Section)
    user_info = await client.get_users(target_user.id)
    if user_info.bio:
        await client.update_profile(bio=user_info.bio)
    
    # ✅ Clone Profile Pictures
    photos = await client.get_profile_photos(target_user.id)
    if photos:
        temp_dir = "cloned_pfp.jpg"
        await client.download_media(photos[0].file_id, temp_dir)  # Download latest profile pic
        await client.set_profile_photo(photo=temp_dir)  # Set as new profile pic
        os.remove(temp_dir)  # Cleanup file after use

    await message.reply(f"✅ **Successfully cloned {target_user.mention}**!")


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
