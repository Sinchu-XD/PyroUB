from Abhi import app, logger

if __name__ == "__main__":
    logger.info("🚀 Starting UserBot...")
    try:
        app.run()  # ✅ This automatically handles event loops
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}", exc_info=True)
