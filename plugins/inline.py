#!/usr/bin/env python3

from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from config import Config
from utils import LOGGER
from pyrogram.types import (
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from pyrogram import (
    Client, 
    errors
)
<p align="center">
  <img src="https://te.legra.ph/file/965b2df3eeaf45cc5a291.jpg"</
) 

buttons = [
    [
        InlineKeyboardButton('🥰 ᴏᴡɴᴇʀ', url='https://t.me/santhu_music_bot),        
        InlineKeyboardButton('😃 ɴᴇᴛᴡᴏʀᴋ', url='https://t.me/santhuvc'),
        InlineKeyboardButton('➕ 𝙽𝙰𝙽𝚄 𝙰𝙳𝙳 𝙲𝙷𝙴𝚂𝚄𝙺𝙾𝙽𝙳𝙸', url='https://t.me/{BOT_USERNAME}?startgroup=true'), 
    ]
    ]
def get_cmd(dur):
    if dur:
        return "/play"
    else:
        return "/stream"
@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "ᴘᴍ ᴄʜᴇʏɪ..":
        answers.append(
            InlineQueryResultArticle(
                title="Deploy",
                input_message_content=InputTextMessageContent(f"{Config.REPLY_MESSAGE}\n\n<b>You can't use this bot in your group, contact @santhu_music_bot.</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("sᴇᴀʀᴄʜ ᴀ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "{} https://www.youtube.com/watch?v={}".format(get_cmd(v["duration"]), v["id"])
                    ),
                    thumb_url=v["thumbnails"][0]["https://te.legra.ph/file/509686aa88a027bffe2b3.jpg"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Nothing found"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
