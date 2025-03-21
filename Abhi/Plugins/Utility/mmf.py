import os
from pyrogram import filters
import textwrap
from PIL import Image, ImageDraw, ImageFont
from Abhi import app


PREFIXES = [".", "!"]


@bot.on_message(filters.command("mmf", PREFIXES) & filters.reply)
async def memeify(client, message):
    reply = message.reply_to_message
    if not reply.photo:
        return await message.reply("Reply to an image with /mmf <text>")
    file = await client.download_media(reply)
    text = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else "Meme Text"
    meme_path = await drawText(file, text)
    await message.reply_photo(meme_path)
    os.remove(meme_path)

def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    font = ImageFont.truetype("arial.ttf", int((70 / 640) * i_width))
    draw = ImageDraw.Draw(img)
    draw.text((i_width / 2, 10), text, font=font, fill="white", anchor="mm")
    meme_file = "memify.webp"
    img.save(meme_file, "WEBP")
    return meme_file
