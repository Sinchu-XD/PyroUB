import asyncio
from Abhi import app, logger

async def run_bot():
    while True:
        try:
            logger.info("🚀 Starting UserBot...")
            await app.start()
            await app.idle()  # ✅ Keeps the bot running
        except Exception as e:
            logger.error(f"❌ Connection lost: {e}. Retrying in 5 seconds...", exc_info=True)
            await asyncio.sleep(5)  # ⏳ Wait before reconnecting

if __name__ == "__main__":
    asyncio.run(run_bot())  # ✅ Async handling of bot reconnection
