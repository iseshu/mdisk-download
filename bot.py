import os
import time
import math
import string
import random
import requests
import ffmpeg_streaming
from ffmpeg_streaming import Formats
from pyrogram import filters, Client
from pyrogram.types.messages_and_media import message
from pyrogram.types import *
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

bot_token = "5578176214:AAHUGftG8LSeo6M8etYBEOqWKXHLZYu-5WM"
get_url = "https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={}"
bot = Client('bot',
             api_id=6789558,
             api_hash="cd22d549f86070dac2068e1659045bde",
             bot_token=bot_token,
             workers=50,
             sleep_threshold=10)

def convert_size(size_bytes):
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id,
                           reply_to_message_id=message.id,
                           text=f"Hello **{message.chat.first_name}!**\nI'm **Mdisk Uploader**\nI'll Upload Mdisk Links Below **2GB**\nJust send me the Mdisk link to upload\nI'm Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton(
                                           "Support 💖", url="https://t.me/yssprojects"),
                                       InlineKeyboardButton(
                                           "Developer 🙍", url="https://t.me/seshu2004")
                                   ]
                               ]
                           )
                           )

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(client, message):
    link = message.matches[0].group(0)
    if "mdisk.me" in link:
        id = link.split("/")[-1]
        url = get_url.format(id)
        res = requests.get(url)
        if res.status_code == 200:
            req = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 6))
            file_name = f"{req}.mp4"
            filename = res.json()["filename"]
            duration = res.json()["duration"]
            height = res.json()["height"]
            width = res.json()["width"]
            reslution = f"{height}x{width}"
            size = res.json()["size"]
            sze = convert_size(int(size))
            source = res.json()["source"]
            if ".mpd" in source:
                await message.reply(f"**Filename** : `{filename}`\n**Reslution** : `{reslution}`\n**Duration** : `{convert(duration)}`\n**Status** : `⏬ Downloading To Server`")
                start_time = time.time()
                video = ffmpeg_streaming.input(source)
                stream = video.stream2file(Formats.h264())
                stream.output(file_name)
                end_time = time.time()
                await message.reply(f"**Filename** : `{filename}`\n**Reslution** : `{reslution}`\n**Duration** : `{convert(duration)}`\n**Time Taken**: `{round(end_time-start_time)} Seconds`\n**Status** : `Downloaded To Server`")

            else:
                await message.reply(f"**Filename** : `{filename}`\n**Reslution** : `{reslution}`\n**Duration** : `{convert(duration)}`\n**Size** : `{convert_size(size)}`\n**Status** :`❌ Failed Video Size > 2GB`")





if __name__ == "__main__":
    bot.run()
