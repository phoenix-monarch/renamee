import random, os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from asyncio import sleep
from time import time
from uuid import uuid4
from gif import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from config import Config
from helper.database import db

async def sendMessage(client, message, text):
    try:
        return await message.reply(text=text, quote=True, disable_web_page_preview=True,
                                    disable_notification=True)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(client, message, text)
    except RPCError as e:
        LOGGER.error(f"{e.NAME}: {e.MESSAGE}")
    except Exception as e:
        LOGGER.error(str(e))

@Client.on_message(filters.command(['start', ]))
async def start(client, message):
    if len(message.command) > 1:
        userid = message.from_user.id
        input_token = message.command[1]
        if not await db.is_user_exist(userid):
            return await sendMessage(client, message, 'wait a minute who are you?')
        data = await db.get_user_data(userid)
        if 'token' not in data or data['token'] != input_token:
            return await sendMessage(client, message, 'This is a token already expired')
        data['token'] = str(uuid4())
        data['time'] = time()
        await db.update_user_data(userid, data)
        await sendMessage(client, message, 'Token refreshed successfully!')
        gifs = os.listdir('./gif')
        await message.reply_animation(
            animation=f'./gif/{random.choice(gifs)}',
            caption=f'**Hi There** `'
        )
    else:
        if message.reply_to_message:
            reply = message.reply_to_message
            user_id = reply.from_user.id  
        else:
            user_id = message.from_user.id  
        if not await db.is_user_exist(user_id):
            return await sendMessage(client, message, 'Who are you?')
        data = await db.get_user_data(user_id)
        if 'time' not in data or time() - data['time'] >= Config.TOKEN_TIMEOUT:
            await sendMessage(client, message, "Please provide a token to renew!")
        else:
            gifs = os.listdir('./gif')
            await message.reply_animation(
                animation=f'./gif/{random.choice(gifs)}',
                caption=f'**Hi There** `'
            )
           
@Client.on_message(filters.command(['ping']))
async def ping(client, message):
    start = time()
    await sendMessage(client, message, "😐😑😶")
    end = time()
    duration = round((end - start) * 1000, 3)
    await sendMessage(client, message, f"Ping: {duration}ms")

            
