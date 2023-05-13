import random, os 
from pyrogram import Client, filters
from asyncio import sleep
from time import time
from uuid import uuid4
from gif import *
from shortener import shorten_url
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from helper.database import db
from config import Config 
LOGGER = Config.LOGGER

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    try:
        if len(message.command) > 1:
            userid = message.from_user.id
            input_token = message.command[1]
            if not await db.is_user_exist(userid):
                await client.send_message(message.chat.id, 'wait a minute who are you?')
                return
            data = await db.get_user_data(userid)
            if 'token' not in data or data['token'] != input_token:
                await client.send_message(message.chat.id, 'This is a token already expired')
                return
            data['token'] = str(uuid4())
            data['time'] = time()
            await db.update_user_data(userid, data)
        else:
            userid = message.from_user.id
            data = await db.get_user_data(userid)
            if data is None or 'token' not in data:
                await client.send_message(message.chat.id, 'Please provide a valid token')
                return
            expire = data.get('time')
            isExpired = (expire is None or expire is not None and (time() - expire) > Config.TOKEN_TIMEOUT)
            if isExpired:
                data['token'] = str(uuid4())
                if expire is not None:
                    del data['time']
                data['time'] = time()
                await db.update_user_data(userid, data)
                url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
                shortened_url = shorten_url(url)  # pass the generated URL to the shorten_url function
                text = "🤣Here is your wedding ring🤣:"
                button = InlineKeyboardButton(text="Start bot", url=shortened_url)
                await message.reply(
                    text=text, reply_markup=InlineKeyboardMarkup([[button]])
                )
                return
        gifs = os.listdir('./gif')
        selected_gif = random.choice(gifs)
        caption = f'Hello {message.from_user.first_name}! Welcome to the bot'
        await message.reply_video(
            video=f'./gif/{selected_gif}',
            caption=caption,
            supports_streaming=True
        )
    except Exception as e:
        LOGGER.error(f"An error occurred while executing: {e}")

@Client.on_message(filters.command(['ping']))
async def ping(client, message):
    start = time()
    await sendMessage(client, message, "😐😑😶")
    end = time()
    duration = round((end - start) * 1000, 3)
    await sendMessage(client, message, f"Ping: {duration}ms")

            
