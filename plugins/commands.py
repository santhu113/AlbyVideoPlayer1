#!/usr/bin/env python3

from utils import LOGGER
from contextlib import suppress
from config import Config
import calendar
import pytz
from datetime import datetime
import asyncio
import os
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, 
    MessageNotModified
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from utils import (
    cancel_all_schedules,
    edit_config, 
    is_admin, 
    leave_call, 
    restart,
    restart_playout,
    stop_recording, 
    sync_to_db,
    update, 
    is_admin, 
    chat_filter,
    sudo_filter,
    delete_messages,
    seek_file
)
from pyrogram import (
    Client, 
    filters
)

IST = pytz.timezone(Config.TIME_ZONE)
if Config.DATABASE_URI:
    from utils import db

HOME_TEXT = "<b>ʜᴇʟʟᴏ..💝 [{}](tg://user?id={}) 🙋‍♂️\n\n💖ɴᴇɴᴜ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴠɪᴅᴇᴏ ʙᴏᴛ ɴɪ 💚 ɴᴀɴᴜ ɢʀᴏᴜᴘ ʟᴏ ᴀᴅᴅ ᴄʜᴇsᴜᴋᴏɴᴅɪ ᴍᴀɴᴄʜɪ ᴠɪᴅᴇᴏ sᴏɴɢs sᴛʀᴇᴀᴍɪɴɢ ᴋᴏsᴀᴍ... ᴘᴏᴡᴇʀᴇᴅ ʙʏ💙: @santhu_music_bot</b>"
admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if len(message.command) > 1:
        if message.command[1] == 'help':
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"💙ᴘʟᴀʏ💖", callback_data='help_play'),
                        InlineKeyboardButton(f"🔰sᴇᴛᴛɪɴɢs🔰", callback_data=f"help_settings"),
                        InlineKeyboardButton(f"💝ʀᴇᴄᴏʀᴅɪɴɢ💝", callback_data='help_record'),
                    ],
                    [
                        InlineKeyboardButton("Scheduling", callback_data="help_schedule"),
                        InlineKeyboardButton("Controling", callback_data='help_control'),
                        InlineKeyboardButton("Admins", callback_data="help_admin"),
                    ],
                    [
                        InlineKeyboardButton(f"💖ᴍɪsᴄ🤎", callback_data='help_misc'),
                        InlineKeyboardButton("💘ɴɪʙʙᴀ ᴄʟᴏsᴇ💝", callback_data="close"),
                    ],
                ]
                )
            await message.reply("ʟᴇᴀʀɴ ᴛᴏ ᴜsᴇ ᴛʜᴇ ᴠᴄᴠɪᴅᴇᴏʙᴏᴛ, sʜᴏᴡɪɴɢ ʜᴇʟᴘ ᴍᴇɴᴜ, ᴄʜᴏᴏsᴇ ғʀᴏᴍ ᴛʜᴇ ʙᴇʟᴏᴡ ᴏᴘᴛɪᴏɴs.ғᴏʀ ᴀɴʏ ʜᴇʟᴘ ᴏʀ ʙᴜɢs ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @santhu_music_bot",
                reply_markup=reply_markup,
                disable_web_page_preview=True
                )
        elif 'sch' in message.command[1]:
            msg=await message.reply("ᴄʜᴇᴄᴋɪɴɢ sᴄʜᴇᴅᴜʟᴇs...✅)
            you, me = message.command[1].split("_", 1)
            who=Config.SCHEDULED_STREAM.get(me)
            if not who:
                return await msg.edit("sᴏᴍᴇᴛʜɪɴɢ ɢᴏɴᴇ sᴏᴍᴇᴡʜᴇʀᴇ.")
            del Config.SCHEDULED_STREAM[me]
            whom=f"{message.chat.id}_{msg.message_id}"
            Config.SCHEDULED_STREAM[whom] = who
            await sync_to_db()
            if message.from_user.id not in Config.ADMINS:
                return await msg.edit("OK da")
            today = datetime.now(IST)
            smonth=today.strftime("%B")
            obj = calendar.Calendar()
            thisday = today.day
            year = today.year
            month = today.month
            m=obj.monthdayscalendar(year, month)
            button=[]
            button.append([InlineKeyboardButton(text=f"{str(smonth)}  {str(year)}",callback_data=f"sch_month_choose_none_none")])
            days=["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
            f=[]
            for day in days:
                f.append(InlineKeyboardButton(text=f"{day}",callback_data=f"day_info_none"))
            button.append(f)
            for one in m:
                f=[]
                for d in one:
                    year_=year
                    if d < int(today.day):
                        year_ += 1
                    if d == 0:
                        k="\u2063"   
                        d="none"   
                    else:
                        k=d    
                    f.append(InlineKeyboardButton(text=f"{k}",callback_data=f"sch_month_{year_}_{month}_{d}"))
                button.append(f)
            button.append([InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="schclose")])
            await msg.edit(f"Choose the day of the month you want to schedule the voicechat.\nToday is {thisday} {smonth} {year}. Chooosing a date preceeding today will be considered as next year {year+1}", reply_markup=InlineKeyboardMarkup(button))



        return
    buttons = [
        [
            InlineKeyboardButton('🤎ᴏᴡɴᴇʀ💖', url='https://t.me/santhu_music_bot'),
            InlineKeyboardButton('💗ɴᴇᴛᴡᴏʀᴋ💝', url='https://t.me/santhuvc')
        ],
        [
            InlineKeyboardButton('❤ʜᴇʟᴘ💝', callback_data='help_main'),
            InlineKeyboardButton('💙ɴɪʙʙᴀ ᴄʟᴏsᴇ❤', callback_data='close'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    k = await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await delete_messages([message, k])



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴘʟᴀʏ", callback_data='help_play'),
                InlineKeyboardButton("sᴇᴛᴛɪɴɢs", callback_data=f"help_settings"),
                InlineKeyboardButton("ʀᴇᴄᴏʀᴅɪɴɢ", callback_data='help_record'),
            ],
            [
                InlineKeyboardButton("sᴄʜᴇᴅᴜʟɪɴɢ", callback_data="help_schedule"),
                InlineKeyboardButton("ᴄᴏɴᴛʀᴏʟɪɴɢ", callback_data='help_control'),
                InlineKeyboardButton("ᴀᴅᴍɪɴs", callback_data="help_admin"),
            ],
            [
                InlineKeyboardButton("ᴍɪsᴄ", callback_data='help_misc'),
                InlineKeyboardButton("ᴄᴏɴғɪɢ ᴠᴀʀs", callback_data='help_env'),
                InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
            ],
        ]
        )
    if message.chat.type != "private" and message.from_user is None:
        k=await message.reply(
            text="ɪ ᴄᴀɴᴛ ʜᴇʟᴘ ʏᴏᴜ ʜᴇʀᴇ, sɪɴᴄᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ. ɢᴇᴛ ʜᴇʟᴘ ɪɴ ᴘᴍ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"🔰ʜᴇʟᴘ🔰", url=f"https://telegram.dog/{Config.BOT_USERNAME}?start=help"),
                    ]
                ]
            ),)
        await delete_messages([message, k])
        return
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        "ʟᴇᴀʀɴ ᴛᴏ ᴜsᴇ ᴛʜᴇ ᴠᴄᴘʟᴀʏᴇʀ, sʜᴏᴡɪɴɢ ʜᴇʟᴘ ᴍᴇɴᴜ, ᴄʜᴏᴏsᴇ ғʀᴏᴍ ᴛʜᴇ ʙᴇʟᴏᴡ ᴏᴘᴛɪᴏɴs.",
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
    #await delete_messages([message])
@Client.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton('❤ᴏᴡɴᴇʀ💘', url='https://t.me/santhu_music_bot'),
            InlineKeyboardButton('💖ɴᴇᴛᴡᴏʀᴋ❤', url='https://t.me/santhuvc'),     
        ],
        [
            InlineKeyboardButton("💗 ʀᴇᴘᴏʀᴛ ʙᴜɢs", url='https://t.me/santhu_music_bot'),
            InlineKeyboardButton('💛 ɴɪʙʙᴀ ᴄʟᴏsᴇ💖', callback_data='close'),
        ]
    ]
    await message.reply("", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await delete_messages([message])

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k = await message.reply("ʜᴇʀᴏᴋᴜ ᴀᴘᴘ ғᴏᴜɴᴅ, ʀᴇsᴛᴀʀᴛɪɴɢ ᴀᴘᴘ ᴛᴏ ᴜᴘᴅᴀᴛᴇ.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
            await sync_to_db()
    else:
        k = await message.reply("ɴᴏ ʜᴇʀᴏᴋᴜ ᴀᴘᴘ ғᴏᴜɴᴅ, ᴛʀʏɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
    try:
        await message.delete()
    except:
        pass
    await update()

@Client.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def get_logs(client, message):
    m=await message.reply("ᴄʜᴇᴄᴋɪɴɢ ʟᴏɢs..")
    if os.path.exists("botlog.txt"):
        await message.reply_document('botlog.txt', caption="ʙᴏᴛ ʟᴏɢs")
        await m.delete()
        await delete_messages([message])
    else:
        k = await m.edit("ɴᴏ ʟᴏɢ ғɪʟᴇs ғᴏᴜɴᴅ.")
        await delete_messages([message, k])

@Client.on_message(filters.command(['env', f"env@{Config.BOT_USERNAME}", "config", f"config@{Config.BOT_USERNAME}"]) & sudo_filter & chat_filter)
async def set_heroku_var(client, message):
    with suppress(MessageIdInvalid, MessageNotModified):
        m = await message.reply("ᴄʜᴇᴄᴋɪɴɢ ᴄᴏɴғɪɢ ᴠᴀʀs..")
        if " " in message.text:
            cmd, env = message.text.split(" ", 1)
            if "=" in env:
                var, value = env.split("=", 1)
            else:
                if env == "STARTUP_STREAM":
                    env_ = "STREAM_URL"
                elif env == "QUALITY":
                    env_ = "CUSTOM_QUALITY" 
                else:
                    env_ = env
                ENV_VARS = ["ADMINS", "SUDO", "CHAT", "LOG_GROUP", "STREAM_URL", "SHUFFLE", "ADMIN_ONLY", "REPLY_MESSAGE", 
                        "EDIT_TITLE", "RECORDING_DUMP", "RECORDING_TITLE", "IS_VIDEO", "IS_LOOP", "DELAY", "PORTRAIT", 
                        "IS_VIDEO_RECORD", "PTN", "CUSTOM_QUALITY"]
                if env_ in ENV_VARS:
                    await m.edit(f"Current Value for `{env}`  is `{getattr(Config, env_)}`")
                    await delete_messages([message])
                    return
                else:
                    await m.edit("This is an invalid env value. Read help on env to know about available env vars.")
                    await delete_messages([message, m])
                    return     
            
        else:
            await m.edit("ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴘʀᴏᴠɪᴅᴇᴅ ᴀɴʏ ᴠᴀʟᴜᴇ ғᴏʀ ᴇɴᴠ, ʏᴏᴜ sʜᴏᴜʟᴅ ғᴏʟʟᴏᴡ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ.\nExample: <code>/env CHAT=-1001655662380</code> to change or set CHAT var.\n<code>/env REPLY_MESSAGE= <code>To delete REPLY_MESSAGE.")
            await delete_messages([message, m])
            return

        if Config.DATABASE_URI and var in ["STARTUP_STREAM", "CHAT", "LOG_GROUP", "REPLY_MESSAGE", "DELAY", "RECORDING_DUMP", "QUALITY"]:      
            await m.edit("ᴍᴏɴɢᴏ ᴅʙ ғᴏᴜɴᴅ, sᴇᴛᴛɪɴɢ ᴜᴘ ᴄᴏɴғɪɢ ᴠᴀʀs...")
            await asyncio.sleep(2)  
            if not value:
                await m.edit(f"No value for env specified. Trying to delete env {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY"]:
                    await m.edit("This is a mandatory var and cannot be deleted.")
                    await delete_messages([message, m]) 
                    return
                await edit_config(var, False)
                await m.edit(f"Sucessfully deleted {var}")
                await delete_messages([message, m])           
                return
            else:
                if var in ["CHAT", "LOG_GROUP", "RECORDING_DUMP", "QUALITY"]:
                    try:
                        value=int(value)
                    except:
                        if var == "QUALITY":
                            if not value.lower() in ["low", "medium", "high"]:
                                await m.edit("ʏᴏᴜ sʜᴏᴜʟᴅ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟᴜᴇ ʙᴇᴛᴡᴇᴇɴ 𝟷𝟶 - 𝟷𝟶𝟶.")
                                await delete_messages([message, m])
                                return
                            else:
                                value = value.lower()
                                if value == "high":
                                    value = 100
                                elif value == "medium":
                                    value = 66.9
                                elif value == "low":
                                    value = 50
                        else:
                            await m.edit("ʏᴏᴜ sʜᴏᴜʟᴅ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄʜᴀᴛ ɪᴅ . ɪᴛ sʜᴏᴜʟᴅ ʙᴇ ᴀɴ ɪɴᴛᴇʀɢᴇʀ.")
                            await delete_messages([message, m])
                            return
                    if var == "CHAT":
                        await leave_call()
                        Config.ADMIN_CACHE=False
                        if Config.IS_RECORDING:
                            await stop_recording()
                        await cancel_all_schedules()
                        Config.CHAT=int(value)
                        await restart()
                    await edit_config(var, int(value))
                    if var == "QUALITY":
                        if Config.CALL_STATUS:
                            data=Config.DATA.get('FILE_DATA')
                            if not data \
                                or data.get('dur', 0) == 0:
                                await restart_playout()
                                return
                            k, reply = await seek_file(0)
                            if k == False:
                                await restart_playout()
                    await m.edit(f"sᴜᴄᴄᴇsғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ {var} to {value}")
                    await delete_messages([message, m])
                    return
                else:
                    if var == "STARTUP_STREAM":
                        Config.STREAM_SETUP=False
                    await edit_config(var, value)
                    await m.edit(f"sᴜᴄᴄᴇsғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ {var} to {value}")
                    await delete_messages([message, m])
                    await restart_playout()
                    return
        else:
            if not Config.HEROKU_APP:
                buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('💝ɴɪʙʙᴀ ᴄʟᴏsᴇ💗', callback_data='close'),]]
                await m.edit(
                    text="No heroku app found, this command needs the following heroku vars to be set.\n\n1. <code>HEROKU_API_KEY</code>: Your heroku account api key.\n2. <code>HEROKU_APP_NAME</code>: Your heroku app name.", 
                    reply_markup=InlineKeyboardMarkup(buttons)) 
                await delete_messages([message])
                return     
            config = Config.HEROKU_APP.config()
            if not value:
                await m.edit(f"ɴᴏ ᴠᴀʟᴜᴇ ғᴏʀ ᴇɴᴠ sᴘᴇᴄɪғɪᴇᴅ. ᴛʀʏɪɴɢ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴇɴᴠ {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY", "API_ID", "API_HASH", "BOT_TOKEN", "SESSION_STRING", "ADMINS"]:
                    await m.edit("ᴛʜᴇsᴇ ᴀʀᴇ ᴍᴀɴᴅᴀᴛᴏʀʏ ᴠᴀʀs ᴀɴᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.")
                    await delete_messages([message, m])
                    return
                if var in config:
                    await m.edit(f"sᴜᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {var}")
                    await asyncio.sleep(2)
                    await m.edit("ɴᴏᴡ ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ᴀᴘᴘ ᴛᴏ ᴍᴀᴋᴇ ᴄʜᴀɴɢᴇs.")
                    if Config.DATABASE_URI:
                        msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                        if not await db.is_saved("RESTART"):
                            db.add_config("RESTART", msg)
                        else:
                            await db.edit_config("RESTART", msg)
                    del config[var]                
                    config[var] = None               
                else:
                    k = await m.edit(f"No env named {var} found. Nothing was changed.")
                    await delete_messages([message, k])
                return
            if var in config:
                await m.edit(f"Variable already found. Now edited to {value}")
            else:
                await m.edit(f"ᴠᴀʀɪᴀʙʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ, ɴᴏᴡ sᴇᴛᴛɪɴɢ ᴀs ɴᴇᴡ ᴠᴀʀ.")
            await asyncio.sleep(2)
            await m.edit(f"sᴜᴄᴄᴇsғᴜʟʟʏ sᴇᴛ {var} with value {value}, ɴᴏᴡ ʀᴇsᴛᴀʀᴛɪɴɢ ᴛᴏ ᴛᴀᴋᴇ ᴇғғᴇᴄᴛ ᴏғ ᴄʜᴀɴɢᴇs...")
            if Config.DATABASE_URI:
                msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                if not await db.is_saved("RESTART"):
                    db.add_config("RESTART", msg)
                else:
                    await db.edit_config("RESTART", msg)
            config[var] = str(value)




