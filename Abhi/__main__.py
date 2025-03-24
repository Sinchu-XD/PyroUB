import asyncio
from Abhi import app, logger

async def run_bot():
    try:
        await app.disconnect()  # Ensures no active session conflict
        await app.start()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(run_bot())  # ✅ Async handling of bot reconnection
