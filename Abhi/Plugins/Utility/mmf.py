import os
import random
import cv2
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

# Paths
FONT_PATH = "Abhi/Plugins/Assets/Impact.ttf"  # Ensure this file exists
TEMP_PATH = "Abhi/Plugins/Temp/"

# Ensure the temp directory exists
os.makedirs(TEMP_PATH, exist_ok=True)

async def generate_meme(client, message: Message, output_type="image"):
    if not message.reply_to_message:
        return await message.reply("❌ **Reply to an image, sticker, or GIF with text!**")

    # Check media type
    media = message.reply_to_message
    if not (media.photo or media.sticker or media.animation):
        return await message.reply("❌ **Only images, stickers, and GIFs are supported!**")

    # Extract meme text
    if len(message.command) < 2:
        return await message.reply("⚠️ **Provide text for the meme!**\nExample: `.mmfimg Top Text | Bottom Text`")

    meme_text = " ".join(message.command[1:]).split("|")
    top_text = meme_text[0].strip() if meme_text[0] else ""
    bottom_text = meme_text[1].strip() if len(meme_text) > 1 else ""

    # Prevent 'NoneType' issues
    if not top_text and not bottom_text:
        return await message.reply("⚠️ **Text cannot be empty!**")

    # Download media
    media_path = await client.download_media(media)
    output_image_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.png")
    output_sticker_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.webp")

    try:
        # Convert GIF/Video Sticker to Image (First Frame)
        if media.animation or (media.sticker and media.sticker.is_video):
            temp_frame = os.path.join(TEMP_PATH, f"frame_{random.randint(1000, 9999)}.jpg")
            cap = cv2.VideoCapture(media_path)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(temp_frame, frame)
                media_path = temp_frame
            else:
                return await message.reply("❌ **Failed to extract a frame from GIF/Video Sticker!**")

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
            if not text or not isinstance(text, str):  # Fix for 'NoneType' error
                return
            x, y = position

            # Calculate text size
            bbox = draw.textbbox((0, 0), text, font=font) if hasattr(draw, "textbbox") else (0, 0, 0, 0)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Ensure text is valid
            if text_width == 0 or text_height == 0:
                return

            # Center text
            x = (img.width - text_width) // 2

            # Draw text outline
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + dx, y + dy), text, font=font, fill="black")

            # Draw main white text
            draw.text((x, y), text, font=font, fill="white")

        # Add texts
        draw_text(draw, top_text, (0, 10))  # Top
        draw_text(draw, bottom_text, (0, img.height - int(img.height / 10) - 10))  # Bottom

        # Save meme in appropriate format
        if output_type == "sticker":
            img = img.convert("RGB")  # Ensure webp format works correctly
            img.save(output_sticker_path, "WEBP")
            await message.reply_sticker(output_sticker_path)
        else:
            img.save(output_image_path)
            await message.reply_photo(output_image_path, caption="😂 **Here's your meme!**")

    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

    finally:
        # Clean up temp files
        if os.path.exists(media_path):
            os.remove(media_path)
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
        if os.path.exists(output_sticker_path):
            os.remove(output_sticker_path)

# Command for Image Output
@app.on_message(filters.command("mmfimg", [".", "!"]) & filters.reply)
async def mmfimg(client, message: Message):
    await generate_meme(client, message, output_type="image")

# Command for Sticker Output
@app.on_message(filters.command("mmfsticker", [".", "!"]) & filters.reply)
async def mmfsticker(client, message: Message):
    await generate_meme(client, message, output_type="sticker")
            
