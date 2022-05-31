from pyrogram import filters, idle
from . import app, get_commands, NAME, ID
from config import *
import asyncio
from .utils import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
PREFIXES = ["/", "!", "."]


@app.on_message(filters.command(get_commands("start"), prefixes=PREFIXES))
async def _start(_, message):
  if message.from_user.id in SUDOERS:
    return await message.reply_text(text = f"I'm [{NAME}](tg://user?id={ID})\nUse /gen - Generate links\nUse/cancel - Cancel current process any time\nUse /restart - Restart Bot")
  else:
    subed = await check_sub(message.from_user.id)
    if not subed:
      fsub = await app.get_chat(FSUB)
      return await message.reply_text(
        text=f"It seems you aren't a participant of {fsub.title}\nTo use me its mandatory to join it in order to use me \nPlease join it and try again later",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton(
                text=f"Join {fsub.title}",
                url=fsub.invite_link
              )
            ]
          ]
        )
      )
    else:
      txt = message.text.split(None, 1)[1]
      txt = txt.split("-")
      if len(txt) == 3:
        start_msg = await decode(txt[1])
        end_msg = await decode(txt[2])
        msgs = await get_ids(start_msg, end_msg)
        await message.reply_text("Please Wait I am getting messages")
        for msg in msgs:
          await app.copy_message(chat_id=message.chat.id, from_chat_id=DB_CHANNEL, message_id=msg)
          await asyncio.sleep(10)
        return await message.reply_text(f"Sent `{len(msgs)}` scheduled messages")
      if len(txt) == 2:
        msg = await decode(txt[1])
        await message.reply_text("Please wait i")
