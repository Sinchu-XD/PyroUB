from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UsernameOccupied, RPCError
from Abhi import app  # Import your bot instance

PREFIXES = [".", "!"]
original_profile = {}  # Store the original profile before cloning


@app.on_message(filters.command("clone", PREFIXES) & filters.private)
async def clone_profile(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply("⚠️ **Reply to a user to clone their profile!**")

    target_user = message.reply_to_message.from_user

    # Save Original Profile Before Cloning
    global original_profile
    me = await client.get_me()
    original_profile = {
        "name": me.first_name,
        "last_name": me.last_name,
        "bio": (await client.get_chat(me.id)).bio,
        "photos": await client.get_profile_photos(me.id)
    }

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
        target_bio = (await client.get_chat(target_user.id)).bio
        if target_bio:
            await client.update_profile(bio=target_bio)

        # Clone Profile Picture
        photos = await client.get_profile_photos(target_user.id)
        if photos:
            photo_path = await client.download_media(photos[0].file_id)
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
    global original_profile

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
            await client.set_profile_photo(photo=await client.download_media(original_profile["photos"][0].file_id))
        else:
            await client.delete_profile_photos()

        await message.reply("🔄 **Profile restored to original settings!**")

    except Exception as e:
        await message.reply(f"⚠️ **Error restoring profile:** `{e}`")
        
