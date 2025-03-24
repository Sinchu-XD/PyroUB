from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID", 25024171))
API_HASH = os.getenv("API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7726535663:AAGWWYg6mOUF3MvsFH1bbEqo43X8JteFm9o")
