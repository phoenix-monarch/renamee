import random
import os
import asyncio
from time import time
from uuid import uuid4
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from config import Config
from shortener import shorten_url

 async def validate_user(client, message):
    userid = message.from_user.id
    data = await db.get_user_data(userid)
    if data is None:
        data = {}
        await db.update_user_data(userid, data)
    input_token = None
    if len(message.command) > 1:
        input_token = message.command[1]
    
    if Config.TOKEN_TIMEOUT:
        expire = data.get('time')
        is_expired = (expire is None or (time() - expire) > Config.TOKEN_TIMEOUT)
        if is_expired:
            data['token'] = str(uuid4())
            data['time'] = time()
            url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
            shortened_url = shorten_url
            button = InlineKeyboardButton(text='Refresh Token', url=shortened_url)
            await db.update_user_data(userid, data)
            await client.send_message(
                chat_id=message.chat.id,
                text='Your token has expired.',
                reply_markup=InlineKeyboardMarkup([[button]])
            )
            return False
    if input_token:
        if 'token' not in data or data['token'] != input_token:
            data['token'] = str(uuid4())
            data['time'] = time()
            await db.update_user_data(userid, data)
            url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
            shortened_url = shorten_url
            button = InlineKeyboardButton(text='Refresh Token', url=shortened_url)
            await client.send_message(
                chat_id=message.chat.id,
                text='Invalid token.',
                reply_markup=InlineKeyboardMarkup([[button]])
            )
            return False
    else:
        if 'token' not in data or is_expired:
            data['token'] = str(uuid4())
            data['time'] = time()
            await db.update_user_data(userid, data)
            url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
            shortened_url = shorten_url
            button = InlineKeyboardButton(text='Get Token', url=shortened_url)
            await client.send_message(
                chat_id=message.chat.id,
                text='You need a token to use this bot.',
                reply_markup=InlineKeyboardMarkup([[button]])
            )
            return False
    return True
