import logging
from pyrogram import Client

# Assuming your Abhi.Config contains API_ID, API_HASH, and BOT_TOKEN
from Abhi.Config import API_ID, API_HASH, BOT_TOKEN

# 🔹 Configure Logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔹 Initialize Pyrogram Bot Client (Important Change)
app = Client(
    "Abhi",  # Change session name to indicate it's a bot
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,  # Use bot_token instead of session_string
    plugins=dict(root="Abhi.Plugins")  # Ensure Plugins Load Correctly
)

logger.info("🔥 Bot is initializing...")

if __name__ == "__main__":
    app.run() #run the bot.
