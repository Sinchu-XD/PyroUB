import os
import random
import cv2
import lottie
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from lottie.exporters import to_pillow
from pyrogram import filters
from pyrogram.types import Message
from Abhi import app  # Your bot instance

# Paths
FONT_PATH = "Abhi/Plugins/Assets/Impact.ttf"
TEMP_PATH = "Abhi/Plugins/Temp/"

# Ensure temp folder exists
os.makedirs(TEMP_PATH, exist_ok=True)

async def convert_tgs_to_webp(tgs_path, output_path):
    """ Converts `.tgs` (Lottie) to `.webp` """
    try:
        animation = lottie.parsers.tgs.parse_tgs_file(tgs_path)
        pillow_frames = to_pillow(animation)  # Convert Lottie to PIL
        first_frame = pillow_frames[0]  # Extract first frame
        first_frame.save(output_path, "WEBP")  # Save as sticker
        return output_path
    except Exception as e:
        print(f"Error converting .tgs: {e}")
        return None

async def convert_gif_or_video(media_path, output_gif_path):
    """ Converts a GIF or Video Sticker to a Processable GIF """
    cap = cv2.VideoCapture(media_path)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))

    cap.release()

    if not frames:
        return None

    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0, duration=50)
    return output_gif_path

async def generate_meme(client, message: Message, output_type="image"):
    if not message.reply_to_message:
        return await message.reply("❌ **Reply to an image, sticker, or GIF with text!**")

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

    media_path = await client.download_media(media)
    output_image_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.png")
    output_sticker_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.webp")
    output_gif_path = os.path.join(TEMP_PATH, f"meme_{random.randint(1000, 9999)}.gif")

    try:
        if media.sticker and media.sticker.is_animated:
            # Convert `.tgs` to `.webp`
            converted_path = await convert_tgs_to_webp(media_path, output_sticker_path)
            if not converted_path:
                return await message.reply("❌ **Failed to convert animated sticker!**")
            media_path = converted_path

        elif media.animation or (media.sticker and media.sticker.is_video):
            # Convert GIF/Video Sticker to processable GIF
            converted_path = await convert_gif_or_video(media_path, output_gif_path)
            if not converted_path:
                return await message.reply("❌ **Failed to convert GIF/Video Sticker!**")
            media_path = converted_path

        # Open image
        img = Image.open(media_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Load font
        try:
            font_size = int(img.height / 10)
            font = ImageFont.truetype(FONT_PATH, size=font_size)
        except:
            return await message.reply("❌ **Impact font missing!** Upload `impact.ttf` to `Assets/` folder.")

        # Function to draw text with outline
        def draw_text(draw, text, position):
            if not text or not isinstance(text, str):
                return
            x, y = position
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
            if text_width == 0 or text_height == 0:
                return
            x = (img.width - text_width) // 2
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((x + dx, y + dy), text, font=font, fill="black")
            draw.text((x, y), text, font=font, fill="white")

        # Add texts
        draw_text(draw, top_text, (0, 10))
        draw_text(draw, bottom_text, (0, img.height - font_size - 10))

        if media.animation or (media.sticker and media.sticker.is_video):
            # Process GIF frames
            frames = []
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA")
                draw = ImageDraw.Draw(frame)
                draw_text(draw, top_text, (0, 10))
                draw_text(draw, bottom_text, (0, frame.height - font_size - 10))
                frames.append(frame)

            frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0, duration=50)
            await message.reply_animation(output_gif_path, caption="😂 **Here's your meme!**")

        else:
            # Save image or sticker
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
        # Clean up temp files
        if os.path.exists(media_path):
            os.remove(media_path)
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
        if os.path.exists(output_sticker_path):
            os.remove(output_sticker_path)
        if os.path.exists(output_gif_path):
            os.remove(output_gif_path)

# Command for Image Output
@app.on_message(filters.command("mmfimg", [".", "!"]) & filters.reply)
async def mmfimg(client, message: Message):
    await generate_meme(client, message, output_type="image")

# Command for Sticker Output
@app.on_message(filters.command("mmfsticker", [".", "!"]) & filters.reply)
async def mmfsticker(client, message: Message):
    await generate_meme(client, message, output_type="sticker")
    
