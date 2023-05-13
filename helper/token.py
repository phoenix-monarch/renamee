from time import time
from uuid import uuid4
from config import Config
from helper.database import db
from shortener import shorten_url
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

async def checking_access(user_id, message):
    if not Config.TOKEN_TIMEOUT:
        return None
    user_data = await db.user_data_col.find_one({'user_id': user_id})
    if user_data is None:
        user_data = {'user_id': user_id, 'data': {}}
        await db.user_data_col.insert_one(user_data)
    else:
        user_data = user_data.copy()
    data = user_data['data']
    expire = data.get('time')
    isExpired = (expire is None or expire is not None and (time() - expire) > Config.TOKEN_TIMEOUT)
    if isExpired:
        token = data.get('token') or str(uuid4())
        if expire is not None:
            del data['time']
        data['token'] = token
        user_data['data'] = data
        await db.user_data_col.update_one({'user_id': user_id}, {'$set': {'data': data}})
    url = f'https://t.me/{Config.BOT_NAME}?start={token}'
    shortened_url = shorten_url(url)  # pass the generated URL to the shorten_url function
    text = "🤣Here is your wedding ring🤣:"
    button = InlineKeyboardButton(text="Start bot", url=shorten_url)
    await message.reply(
        text=text,
        reply_markup=InlineKeyboardMarkup([[button]])
    )
