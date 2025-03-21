import os
import random
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

# Font path (ensure this file exists in your bot directory)
FONT_PATH = "Abhi/Plugins/Assets/impact.ttf"
TEMP_PATH = "Abhi/Plugins/Temp/"

# Ensure the temporary folder exists
os.makedirs(TEMP_PATH, exist_ok=True)

@app.on_message(filters.command("mmf", [".", "!"]) & filters.reply)
async def mmf(client, message: Message):
    if not message.reply_to_message.media:
        return await message.reply("⚠️ **Reply to an image or sticker with your text!**")

    if not message.reply_to_message.photo and not message.reply_to_message.sticker:
        return await message.reply("❌ **Only Images and Stickers are supported!**")

    # Extract text
    if len(message.command) < 2:
        return await message.reply("⚠️ **Provide text for the meme!**\nExample: `.mmf Top Text | Bottom Text`")

    meme_text = " ".join(message.command[1:]).split("|")
    top_text = meme_text[0].strip() if len(meme_text) > 0 else ""
    bottom_text = meme_text[1].strip() if len(meme_text) > 1 else ""

    # Download media
    media_path = await client.download_media(message.reply_to_message)
    meme_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.png")

    try:
        # Open the image
        img = Image.open(media_path).convert("RGBA")

        # Resize image for better text fitting
        img = img.resize((500, int(500 * img.height / img.width)))

        # Load font
        try:
            font = ImageFont.truetype(FONT_PATH, 40)
        except:
            return await message.reply("❌ **Font file missing!** Upload `impact.ttf` to `Assets/` folder.")

        draw = ImageDraw.Draw(img)

        # Define text positions
        w, h = img.size
        padding = 10

        def draw_text(text, position):
            text_w, text_h = draw.textsize(text, font=font)
            x = (w - text_w) // 2
            y = position
            draw.text((x + 2, y + 2), text, font=font, fill="black")  # Shadow
            draw.text((x, y), text, font=font, fill="white")  # Main text

        # Add top and bottom text
        if top_text:
            draw_text(top_text, padding)
        if bottom_text:
            draw_text(bottom_text, h - 50 - padding)

        # Save the meme
        img.save(meme_path)

        await message.reply_photo(meme_path, caption="😂 **Here's your meme!**")

    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

    finally:
        # Clean up temporary files
        if os.path.exists(media_path):
            os.remove(media_path)
        if os.path.exists(meme_path):
            os.remove(meme_path)
        
