import random, os, asyncio, uuid
from time import time
from pyrogram.types import InlineKeyboardButton
from helper.database import db
from config import Config
from shortener import shorten_url

async def none_admin_utils(message):
    error_msg = []
    error_button = None
    token_msg, button = await validate_user(message.from_user.id, button)
    if token_msg is not None:
        error_msg.append(token_msg)
        error_button = button    
    return error_msg, error_button

async def validate_user(message, button=None):
    if not Config.TOKEN_TIMEOUT:
        return None, button
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
        if button is None:
            button = InlineKeyboardButton(text='Refresh Token', url=shorten_url(f'https://t.me/{Config.BOT_NAME}?start={token}'))
        
        error_msg = 'Token is expired, refresh your token and try again.'
        return error_msg, button
    
    return None, button
