from __future__ import unicode_literals

import os
import requests
import aiohttp
import yt_dlp
import asyncio
import math
import time

import wget
import aiofiles

from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song'))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**ѕ𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 ѕ𝗈𝗇𝗀...!**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        performer = f"[ 𝖡𝗒 - 𝖫𝖴𝖳𝖳𝖠𝖯𝖯𝖨™]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**𝖿𝗈𝗎𝗇𝖽 𝗇𝗈𝗍𝗁𝗂𝗇𝗀 𝗉𝗅𝖾𝖺𝗌𝖾 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝗍𝗁𝖾 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝗋 𝗌𝖾𝖺𝗋𝖼𝗁 𝖺𝗇𝗒 𝗈𝗍𝗁𝖾𝗋 𝗌𝗈𝗇𝗀**"
        )
        print(str(e))
        return
    m.edit("**𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 ѕ𝗈𝗇𝗀...!**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**𝗃𝗈𝗂𝗇 - [𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/Luttappi_Bot_Update)**\n**𝗉𝗈𝗐𝖾𝗋𝖾𝖽 𝖡𝗒 - [𝖫𝖴𝖳𝖳𝖠𝖯𝖯𝖨 𝖡𝖮𝖳](https://t.me/Luttappi_RoBot)**\n@Luttappi_RoBot**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode=enums.ParseMode.MARKDOWN,quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**🚫 𝖤𝖱𝖱𝖮𝖱 🚫**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**𝖿𝗂𝗇𝖽𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗏𝗂𝖽𝖾𝗈** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖿𝖺𝗂𝗅𝖾𝖽 𝗉𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇..♥️** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""
**𝗍𝗂𝗍𝗅𝖾 :** [{thum}]({mo})
**𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖡𝗒 :** {message.from_user.mention}
**@Luttappi_RoBot**
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,        
        reply_to_message_id=message.id 
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
