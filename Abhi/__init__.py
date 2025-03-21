import logging
from pyrogram import Client
from .Config import API_ID, API_HASH, SESSION_STRING

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Abhi")

# Initialize Pyrofork Client
app = Client(
    "Abhi",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    plugins=dict(root="Abhi.plugins")  # Load plugins from 'Abhi/plugins'
)
