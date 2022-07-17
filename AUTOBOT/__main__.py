from pyrogram import filters, idle
from . import app, get_commands, NAME, ID, USERNAME 
from pyromod import listen
from config import *
import asyncio
from .utils import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
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
        await message.reply_text("**Please Wait I am getting messages**")
        for msg in msgs:
          await app.copy_message(chat_id=message.chat.id, from_chat_id=DB_CHANNEL, message_id=msg)
          await asyncio.sleep(10)
        return await message.reply_text(f"**Sent** `{len(msgs)}` **scheduled messages**")
      if len(txt) == 2:
        msg = await decode(txt[1])
        await message.reply_text("**Please Wait I am Getting the message**")
        await app.copy_message(chat_id=message.chat.id, from_chat_id=DB_CHANNEL, message_id=msg)
        return await message.reply_text("**Sent scheduled message**")


@app.on_message(filters.command(get_commands("restart"), prefixes=PREFIXES) & filters.user(SUDOERS))
async def restart(_, message):
  os.system(f"pkill -9 {os.getpid()}")
  return



@app.on_message(filters.command(get_commands("gen"), prefixes=PREFIXES) & filters.user(SUDOERS))
async def gen(_, message):
  text = "**Please Select Number Of Files to create link**"
  buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text="Single Message", callback_data="singlegen")], [InlineKeyboardButton(text="Multiple Messages", callback_data="multigen")]])
  return await message.reply_text(text=text, reply_markup=buttons)


@app.on_callback_query()
async def callbacks(_, query):
  qd = query.data
  qm = query.message
  if qd == "singlegen":
    await query.message.delete()
    msg = await app.ask(chat_id=query.chat.id, text="Please Forward message from DB_CHANNEL", reply_markup=ForceReply)
    if msg.text:
      if ms == "/cancel":
        return await msg.reply('Process Cancelled')
      else:
        return await msg.reply_text('Please forward message')
    elif not msg.forward_from:
      try:
        x = await msg.copy(DB_CHANNEL)
        link = await encode(f"{x.id}")
        url = f"https://{USERNAME}?start=get_{link}"
        await x.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
        return await msg.reply_text(text=f"Share Url Formed successfully \n\n`{url}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
      except Exception:
        print(Exception)
        return await msg.reply_text(f"**An Exception occured**\n\n__{Exception}__")
    elif msg.forward_from:
      if msg.forward_from_chat:
        if msg.forward_from_chat.id == DB_CHANNEL:
          try:
            mess = await app.get_messages(DB_CHANNEL, messages_id=msg.forward_from_message_id)
            
            link= f"{mess.id}"
            url = f'https://{USERNAME}?start=get_{link}'
            await mess.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
            return await msg.reply_text(text=f"Share Url Formed successfully \n\n`{url}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
          except Exception:
            print(Exception)
            return await msg.reply_text(f"**An Exception occured**\n\n__{Exception}__")
        else:
          return await msg.reply_text("Not Forward from DB CHANNEL")
      else:
        try:
          x = await msg.copy(DB_CHANNEL)
          link = await encode(f"{x.id}")
          url = f"https://{USERNAME}?start=get_{link}"
          await x.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
          return await msg.reply_text(text=f"Share Url Formed successfully \n\n`{url}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
        except Exception:
          print(Exception)
          return await msg.reply_text(f"**An Exception occured**\n\n__{Exception}__")
  elif qd == "multigen":
    await query.message.delete()
      msg = await app.ask(chat_id=query.chat.id, text=f"Please Forward The Starting Message from DB CHANNEL")
      if msg.text: 
        return await msg.reply_text("Process Cancelled ")
    try:
      x = await app.get_messages(chat_id=DB_CHANNEL, message_ids=msg.forward_from_message_id)
      link = await encode(f"{x.id}")
      url = f"https://{USERNAME}?start=get_{link}"
      await x.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
      msg2 = await  app.ask(chat_id=query.chat.id, text=f"Please Forward The Last Message from DB CHANNEL")
      if msg2.text:
        return await msg2.reply_text("Process Cancelled")
      x2 = await app.get_messages(chat_id=DB_CHANNEL, message_ids=msg.forward_from_message_id)
      link2 = await encode(f"{x2.id}")
      url2 = f"https://{USERNAME}?start=get_{link2}"
      await x.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url2}")]]))
      url = f"https://{USERNAME}?start=get_{link}_{link2}"
      return await msg.reply_text(text=f"Share Url Formed successfully \n\n`{url}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Share Url", url=f"https://t.me/share/url?url={url}")]]))
    except Exception:
      print(Exception)
      return await msg.reply_text(f"**An Exception occured**\n\n__{Exception}__")


if __name__ == "__main__":
  idle()
