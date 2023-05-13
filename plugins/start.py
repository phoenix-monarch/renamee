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
        userid = message.from_user.id
        data = await db.get_user_data(userid)
        if data is None:
            data = {}
            await db.update_user_data(userid, data)
        if Config.TOKEN_TIMEOUT:
            expire = data.get('time')
            isExpired = (expire is None or (time() - expire) > Config.TOKEN_TIMEOUT)
            if isExpired:
                data['token'] = str(uuid4())
                data['time'] = time()
                await db.update_user_data(userid, data)
                url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
                shortened_url = shorten_url(url)
                button = InlineKeyboardButton(text='Refresh Token', url=shortened_url)
                await client.send_message(
                    chat_id=message.chat.id,
                    text='Token is expired, refresh your token and try again.',
                    reply_markup=InlineKeyboardMarkup([[button]])
                )
                return
        if len(message.command) > 1:
            input_token = message.command[1]
            if 'token' not in data or data['token'] != input_token:
                await client.send_message(
                    chat_id=message.chat.id,
                    text='Invalid or expired token.'
                )
                return
            data['token'] = str(uuid4())
            data['time'] = time()
            await db.update_user_data(userid, data)
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
    sent_message = await message.reply("😐😑😶")
    end = time()
    duration = round((end - start) * 1000, 3)
    await sent_message.edit_text(f"😶😑😏: {duration}ms")
          
