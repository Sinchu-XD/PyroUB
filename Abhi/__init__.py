import logging
from pyrogram import Client
import os
from Abhi.Config import API_ID, API_HASH, SESSION_STRING

# 🔹 Configure Logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔹 Initialize Pyrogram Client
app = Client(
    "Abhi",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    plugins=dict(root="Abhi.Plugins")  # Ensure Plugins Load Correctly
)

logger.info("🔥 UserBot is initializing...")
