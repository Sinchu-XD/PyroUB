import asyncio
from Abhi import app
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Abhi")


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
  
