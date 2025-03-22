import os
import random
import cv2
import json
import lottie
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Import your bot instance

# Paths
FONT_PATH = "Abhi/Plugins/Assets/Impact.ttf"  # Ensure this file exists
TEMP_PATH = "Abhi/Plugins/Temp/"

# Ensure the temp directory exists
os.makedirs(TEMP_PATH, exist_ok=True)

async def convert_tgs_to_webp(tgs_path, output_path):
    """ Converts `.tgs` (Lottie) files to `.webp` format """
    try:
        animation = lottie.parsers.tgs.parse_tgs(tgs_path)
        frame = animation.render_frame(0)  # Extract first frame as static
        frame.save(output_path, "WEBP")
        return output_path
    except Exception as e:
        print(f"Error converting .tgs: {e}")
        return None

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
    top_text = meme_text[0].strip() if len(meme_text) > 0 else ""
    bottom_text = meme_text[1].strip() if len(meme_text) > 1 else ""

    if not top_text and not bottom_text:
        return await message.reply("⚠️ **Text cannot be empty!**")

    # Download media
    media_path = await client.download_media(media)
    output_image_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.png")
    output_sticker_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.webp")
    output_gif_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.gif")

    try:
        # Handle `.tgs` (Animated Stickers)
        if media.sticker and media.sticker.is_animated:
            webp_path = media_path.replace(".tgs", ".webp")
            converted_path = await convert_tgs_to_webp(media_path, webp_path)

            if not converted_path:
                return await message.reply("❌ **Failed to process animated sticker!**")

            media_path = converted_path  # Replace path with converted file

        # Handle GIFs and video stickers
        if media.animation or (media.sticker and media.sticker.is_video):
            cap = cv2.VideoCapture(media_path)
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                frames.append(img)

            cap.release()
            if not frames:
                return await message.reply("❌ **Failed to extract frames from GIF/Video Sticker!**")

            processed_frames = []
            font_size = int(frames[0].height / 10)
            try:
                font = ImageFont.truetype(FONT_PATH, size=font_size)
            except Exception:
                return await message.reply("❌ **Impact font missing!** Upload `impact.ttf` to `Assets/` folder.")

            def draw_text(draw, text, position, img):
                if not text:
                    return
                x, y = position
                text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
                x = (img.width - text_width) // 2
                for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    draw.text((x + dx, y + dy), text, font=font, fill="black")
                draw.text((x, y), text, font=font, fill="white")

            for frame in frames:
                draw = ImageDraw.Draw(frame)
                draw_text(draw, top_text, (0, 10), frame)
                draw_text(draw, bottom_text, (0, frame.height - font_size - 10), frame)
                processed_frames.append(frame)

            processed_frames[0].save(output_gif_path, save_all=True, append_images=processed_frames[1:], loop=0, duration=50)
            await message.reply_animation(output_gif_path, caption="😂 **Here's your meme!**")

        else:
            img = Image.open(media_path).convert("RGBA")
            draw = ImageDraw.Draw(img)

            try:
                font_size = int(img.height / 10)
                font = ImageFont.truetype(FONT_PATH, size=font_size)
            except Exception:
                return await message.reply("❌ **Impact font missing!** Upload `impact.ttf` to `Assets/` folder.")

            def draw_text(draw, text, position):
                if not text:
                    return
                x, y = position
                text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
                x = (img.width - text_width) // 2
                for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    draw.text((x + dx, y + dy), text, font=font, fill="black")
                draw.text((x, y), text, font=font, fill="white")

            draw_text(draw, top_text, (0, 10))
            draw_text(draw, bottom_text, (0, img.height - font_size - 10))

            if output_type == "sticker":
                img = img.convert("RGB")
                img.save(output_sticker_path, "WEBP")
                await message.reply_sticker(output_sticker_path)
            else:
                img.save(output_image_path)
                await message.reply_photo(output_image_path, caption="😂 **Here's your meme!**")

    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")

    finally:
        if os.path.exists(media_path):
            os.remove(media_path)
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
        if os.path.exists(output_sticker_path):
            os.remove(output_sticker_path)
        if os.path.exists(output_gif_path):
            os.remove(output_gif_path)

@app.on_message(filters.command("mmf", [".", "!"]) & filters.reply)
async def mmfimg(client, message: Message):
    await generate_meme(client, message, output_type="image")

@app.on_message(filters.command("mmfs", [".", "!"]) & filters.reply)
async def mmfsticker(client, message: Message):
    await generate_meme(client, message, output_type="sticker")
    
