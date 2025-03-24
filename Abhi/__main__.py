import asyncio
from Abhi import app, logger

async def run_bot():
    try:
        if not app.is_connected:
            await app.connect()  # Connect only if it's not connected
        
        if not app.is_running:
            await app.start()  # Start only if it's not already running

        logger.info("🔥 Bot is running...")

        await asyncio.Event().wait()  # Keeps the bot running
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        if app.is_connected:
            await app.stop()  # Stop only if it's still connected
        logger.info("🚀 Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # Correct way to start Pyrogram
    except KeyboardInterrupt:
        logger.info("🔴 Bot stopped manually.")
        
