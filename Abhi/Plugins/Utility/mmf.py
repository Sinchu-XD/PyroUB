
import os
import random
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

# Paths
FONT_PATH = "Abhi/Plugins/Assets/Impact.ttf"
TEMP_PATH = "Abhi/Plugins/Temp/"

# Ensure the temp directory exists
os.makedirs(TEMP_PATH, exist_ok=True)

@app.on_message(filters.command("mmf", [".", "!"]) & filters.reply)
async def mmf(client, message: Message):
    if not message.reply_to_message.photo and not message.reply_to_message.sticker:
        return await message.reply("❌ **Reply to an image or sticker with text!**")

    # Extract meme text
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
        draw = ImageDraw.Draw(img)

        # Load font (Fallback if missing)
        try:
            font = ImageFont.truetype(FONT_PATH, size=int(img.height / 10))
        except IOError:
            return await message.reply("❌ **Impact font missing!** Upload `impact.ttf` to `Assets/` folder.")

        # Function to draw outlined text
        def draw_text(draw, text, position):
            if not text:
                return
            x, y = position

            # Calculate text size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Center text
            x = (img.width - text_width) // 2

            # Text outline
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + dx, y + dy), text, font=font, fill="black")

            # Main white text
            draw.text((x, y), text, font=font, fill="white")

        # Add texts
        draw_text(draw, top_text, (0, 10))  # Top
        draw_text(draw, bottom_text, (0, img.height - int(img.height / 10) - 10))  # Bottom

        # Save the meme
        img.save(meme_path)

        # Send meme
        await message.reply_photo(meme_path, caption="😂 **Here's your meme!**")

    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

    finally:
        # Clean up temp files
        if os.path.exists(media_path):
            os.remove(media_path)
        if os.path.exists(meme_path):
            os.remove(meme_path)
            
