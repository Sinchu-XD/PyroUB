from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID", 25024171))
API_HASH = os.getenv("API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
SESSION_STRING = os.getenv("BOT_TOKEN", "7726535663:AAFVBNgn5z-gUK7Tr7XoKTS3bopW3OLBSPM")
