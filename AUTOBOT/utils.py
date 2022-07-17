import base64
from AUTOBOT import app
from config import FSUB
from pyrogram.errors import UserNotParticipant


async def encode(stri):
  stri = stri.encode("ascii")
  stri = base64.b64encode(stri)
  stri = stri.decode("ascii")
  return stri

async def decode(stri):
  stri = stri.encode("ascii")
  stri = base64.b64decode(stri)
  stri = stri.decode("ascii")
  return stri

  
async def get_ids(strt, end):
  ids = []
  for a in range(end - strt +1):
    id = strt + a
    ids.append(int(id))
  return ids

async def check_sub(user):
  try:
    is_user = await app.get_chat_member(FSUB, user)
  except UserNotParticipant:
    return False
  return True
