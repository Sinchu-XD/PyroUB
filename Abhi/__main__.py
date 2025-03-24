import asyncio
from Abhi import app, logger

async def run_bot():
    try:
        if not app.is_connected:
            await app.connect()
        await app.start()
        logger.info("🔥 Bot is running...")

        await asyncio.Event().wait()  # Keeps bot running
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        await app.stop()
        logger.info("🚀 Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # Correct way to start Pyrogram
    except KeyboardInterrupt:
        logger.info("🔴 Bot stopped manually.")
        
