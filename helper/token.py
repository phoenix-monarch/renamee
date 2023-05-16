import random, os, asyncio, uuid
from time import time
from uuid import uuid4
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from config import Config
from shortener import shorten_url

async def validate_user(client, message):
    if not Config.TOKEN_TIMEOUT:
        return None
    userid = message.from_user.id
    data = await db.get_user_data(userid)
    expire = data.get('time')
    is_expired = (expire is None or (time() - expire) > Config.TOKEN_TIMEOUT)
    if is_expired:
        token = data.get('token') if expire is None and 'token' in data else str(uuid.uuid4())
        if expire is not None:
            del data['time']
        data['token'] = token
        await db.update_user_data(userid, data)
        url = f'https://t.me/{Config.BOT_NAME}?start={data["token"]}'
        shortened_url = await shorten_url(url)
        button = InlineKeyboardButton(text='Refresh Token', url=shortened_url)
        return 'Token is expired, refresh your token and try again.', button
    return None
