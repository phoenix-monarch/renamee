import random, os, asyncio 
from time import time
from uuid import uuid4
from shortener import shorten_url
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from helper.database import db
from config import Config 

async def validate_user(client, message):
    userid = message.from_user.id
    data = await db.get_user_data(userid)
    if data is None:
        data = {}
        await db.update_user_data(userid, data)
    input_token = None
    if Config.TOKEN_TIMEOUT:
        expire = data.get('time')
        isExpired = (expire is None or (time() - expire) > Config.TOKEN_TIMEOUT)
        if isExpired:
            data['token'] = str(uuid4())
            url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
            shortened_url = shorten_url(url)
            button = InlineKeyboardButton(text='Refresh Token', url=shortened_url)
            await client.send_message(
                chat_id=message.chat.id,
                text='Your token has expired. Please renew it using the button below.',
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        if len(message.command) > 1:
            input_token = message.command[1]
        while True:
            if 'token' not in data or data['token'] != input_token:
                data['token'] = str(uuid4())
                data['time'] = time()
                await db.update_user_data(userid, data)
            else:
                break
    else:
        data['token'] = str(uuid4())
        data['time'] = time()
        await db.update_user_data(userid, data)
