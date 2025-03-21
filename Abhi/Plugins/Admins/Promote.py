from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges
from Abhi import app

# Define prefixes
PREFIXES = [".", "!"]

# 🌟 Promote User (Basic Admin)
@app.on_message(filters.command("promote", PREFIXES) & filters.group)
async def promote(client, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply To A User To Promote Them!**")
    
    user_id = message.reply_to_message.from_user.id

    # Basic admin privileges
    await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(
        can_manage_chat=True, can_change_info=False, can_delete_messages=True,
        can_invite_users=True, can_restrict_members=False, can_pin_messages=True,
        can_promote_members=False
    ))

    await message.reply(f"🌟 **Congratulations!**\n👑 {message.reply_to_message.from_user.mention} **Has Been Promoted To Admin!** 🎉")

# 🚀 Full Promote (All Admin Privileges)
@app.on_message(filters.command("fullpromote", PREFIXES) & filters.group)
async def full_promote(client, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply To A User To Fully Promote Them!**")
    
    user_id = message.reply_to_message.from_user.id

    # Grant all admin privileges
    await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(
        can_manage_chat=True, can_change_info=True, can_delete_messages=True,
        can_invite_users=True, can_restrict_members=True, can_pin_messages=True,
        can_promote_members=True
    ))

    await message.reply(f"🚀 **Ultimate Power Unlocked!**\n🦸‍♂️ {message.reply_to_message.from_user.mention} **is now a Super Admin!** 🔥")

# ❌ Demote User (Remove Admin Privileges)
@app.on_message(filters.command("demote", PREFIXES) & filters.group)
async def demote(client, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply To A User To Demote Them!**")
    
    user_id = message.reply_to_message.from_user.id

    # Remove all admin privileges
    await client.promote_chat_member(message.chat.id, user_id, ChatPrivileges(
        can_manage_chat=False, can_change_info=False, can_delete_messages=False,
        can_invite_users=False, can_restrict_members=False, can_pin_messages=False,
        can_promote_members=False
    ))

    await message.reply(f"❌ **Admin Rights Revoked!**\n😔 {message.reply_to_message.from_user.mention} **has been demoted to a normal user!**")

# 🔥 Set Admin Title (After Promotion)
@app.on_message(filters.command("title", PREFIXES) & filters.group)
async def setadmin(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ **Usage:** `.title <new admin title>`")
    if not message.reply_to_message:
        return await message.reply("⚠️ **Reply To A User To Set Their Admin Title**")

    user_id = message.reply_to_message.from_user.id
    new_title = message.text.split(None, 1)[1]

    await client.set_administrator_title(message.chat.id, user_id, new_title)

    await message.reply(f"🏅 **Admin Title Updated!**\n🔖 {message.reply_to_message.from_user.mention} **Is Now Titled:** `{new_title}`")
    
