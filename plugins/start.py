import random
import os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from asyncio import sleep
from time import time
from uuid import uuid4
from gif import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from config import Config
from helper.database import db
from helper.token import checking_access

async def sendMessage(client, message, text):
    try:
        return await message.reply_text(
            text=text,
            quote=True,
            disable_web_page_preview=True,
            disable_notification=True
        )
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(client, message, text)
    except RPCError as e:
        LOGGER.error(f"{e.NAME}: {e.MESSAGE}")
    except Exception as e:
        LOGGER.error(str(e))
        print(f"An error occurred while executing: {e}")

@Client.on_message(filters.command(['start']))
async def start(client, message):
    try:
        if len(message.command) > 1:
            userid = message.from_user.id
            input_token = message.command[1]
            if not await db.is_user_exist(userid):
                return await sendMessage(client, message, 'wait a minute who are you?')
            data = await db.get_user_data(userid)
            if 'token' not in data or data['token'] != input_token:
                return await sendMessage(client, message, 'This is a token already expired')
            await checking_access(userid, message)
            data = await db.get_user_data(userid)
        gifs = os.listdir('./gif')
        await message.reply_animation(
            animation=f'./gif/{random.choice(gifs)}',
            caption=f'**Hi There** `'
        )
    except Exception as e:
        LOGGER.error(str(e))
        print(f"An error occurred while executing: {e}")

@Client.on_message(filters.command(['ping']))
async def ping(client, message):
    start = time()
    await sendMessage(client, message, "😐😑😶")
    end = time()
    duration = round((end - start) * 1000, 3)
    await sendMessage(client, message, f"Ping: {duration}ms")

            
