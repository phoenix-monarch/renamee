import random, os, asyncio 
from pyrogram import Client, filters
from time import time
from uuid import uuid4
from gif import *
from shortener import shorten_url
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from helper.database import db
from config import Config 
LOGGER = Config.LOGGER

async def validate_user(client, message):
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
            return False
    if len(message.command) > 1:
        input_token = message.command[1]
        if 'token' not in data or data['token'] != input_token:
            await client.send_message(
                chat_id=message.chat.id,
                text='Invalid or expired token.'
            )
            return False
        data['token'] = str(uuid4())
        data['time'] = time()
        await db.update_user_data(userid, data)
    return True

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    try:
        is_valid = await validate_user(client, message)
        if not is_valid:
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
        print(f"An error occurred while executing start: {e}")
    
@Client.on_message(filters.private & filters.command(['ping']))
async def ping(client, message):
    try:
        is_valid = await validate_user(client, message)
        if not is_valid:
            return
        start = time()
        sent_message = await message.reply("😐😑😶")
        await asyncio.sleep(3)
        end = time()
        duration = round((end - start) * 1000, 3)
        await sent_message.edit_text(f"😶😑😏: {duration}ms")
    except Exception as e:
        print(f"An error occurred while executing ping: {e}")
