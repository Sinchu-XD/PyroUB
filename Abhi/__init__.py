import logging
from pyrogram import Client
from .Config import API_ID, API_HASH, SESSION_STRING

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Abhi")

# Initialize Pyrofork Client
app = Client(
    session_string=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="Plugins"),  # Load plugins from the "plugins" directory
)
