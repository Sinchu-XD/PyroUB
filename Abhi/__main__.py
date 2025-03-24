import asyncio
from Abhi import app, logger

async def run_bot():
    try:
        if app.is_connected:
            logger.warning("⚠️ Bot is already running! Stopping previous session...")
            await app.stop()  # Stop existing session first

        await app.start()  # Start a fresh session
        logger.info("🔥 Bot is running...")

        await asyncio.Event().wait()  # Keep bot running
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        if app.is_connected:  # Only stop if it's still connected
            await app.stop()
            logger.info("🚀 Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # Correct way to start Pyrogram
    except KeyboardInterrupt:
        logger.info("🔴 Bot stopped manually.")
