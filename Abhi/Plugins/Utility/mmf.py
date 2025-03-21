import os
from pyrogram import Client, filters
import textwrap
from PIL import Image, ImageDraw, ImageFont
from Abhi import app

PREFIXES = [".", "!"]

@app.on_message(filters.command("mmf", PREFIXES) & filters.reply)
async def memeify(client, message):
    reply = message.reply_to_message
    if not reply.photo:
        return await message.reply("⚠️ **Reply to an image with .mmf <text>**")

    file = await client.download_media(reply)
    
    if not file:
        return await message.reply("❌ **Failed to download the image!**")

    if len(message.text.split()) > 1:
        text = message.text.split(" ", 1)[1]
    else:
        return await message.reply("⚠️ **You must provide text for the meme!**")

    meme_path = drawText(file, text)
    await message.reply_photo(meme_path)
    
    os.remove(meme_path)

def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)  # Remove the original downloaded image
    i_width, i_height = img.size

    # Use a default font that exists
    font_path = "arial.ttf" if os.name == "nt" else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = int((70 / 640) * i_width)
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(img)

    # Center text manually
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (i_width - text_width) // 2
    text_y = int(0.1 * i_height)  # Adjust position at the top

    # Outline effect for better visibility
    shadow_color = "black"
    draw.text((text_x - 2, text_y - 2), text, font=font, fill=shadow_color)
    draw.text((text_x + 2, text_y - 2), text, font=font, fill=shadow_color)
    draw.text((text_x - 2, text_y + 2), text, font=font, fill=shadow_color)
    draw.text((text_x + 2, text_y + 2), text,
