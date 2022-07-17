from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TOKEN = getenv("BOT_TOKEN")
DB_CHANNEL = getenv("DB_CHANNEL")
FSUB = getenv("FSUB_CHANNEL")
SUDOERS = list(map(int, getenv("SUDOERS").split()))
