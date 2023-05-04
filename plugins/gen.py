from config import config
from helper.database import db
from helper import short_url
from time import time
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton

@Client.on_message(filters.private & filters.command("gen"))
async def gen(client, message):
    user_id = message.chat.id
    if not config['TOKEN_TIMEOUT']:
        return None, None
    user_data = await db.get_user_data(user_id)
    data = user_data.get('data', {})
    expire = data.get('time')
    isExpired = (expire is None or expire is not None and (time() - expire) > config['TOKEN_TIMEOUT'])
    if isExpired:
        token = data.get('token') or str(uuid4())
        if expire is not None:
            del data['time']
        data['token'] = token
        user_data['data'] = data
        await db.update_user_data(user_id, user_data['data'])
    buttons = [InlineKeyboardButton(text="Refresh Token", short_url=f'https://t.me/{bot_name}?start={token}')]
    text = "Token is expired, refresh your token and try again."
    return text, buttons
