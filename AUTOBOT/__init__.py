from pyrogram import Client
from config import *

app = Client(
  "AUTOBOT",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=TOKEN
)

print("[INFO]: STARTING BOT")
app.start()

print("[INFO]: GATHERING PROFILE INFO")
x = app.get_me()
NAME = x.first_name
USERNAME = x.username
ID = x.id
