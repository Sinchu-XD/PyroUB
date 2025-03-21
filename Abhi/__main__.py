import asyncio
import logging
from pyrogram import Client
from .config import API_ID, API_HASH, SESSION_NAME

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Abhi")

# Initialize Pyrofork Client
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="Plugins"),  # Load plugins from the "plugins" directory
)

async def start_bot():
    try:
        await app.start()
        me = await app.get_me()
        logger.info(f"UserBot started successfully as {me.first_name} ({me.id})")
        await asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        await app.stop()

if __name__ == "__main__":
    asyncio.run(start_bot())
  
