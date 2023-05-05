from config import Config
from helper import database as db
from shortener import short_url as url
from time import time
from uuid import uuid4
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.private & filters.command("gen"))
async def gen(client, message):
    try:
        user_id = message.chat.id
        if not Config.TOKEN_TIMEOUT:
            return
        user_data = await db.get_user_data(user_id)
        data = user_data.get('data', {})
        expire = data.get('time')
        isExpired = (expire is None or expire is not None and (time() - expire) > Config.TOKEN_TIMEOUT)
        if isExpired:
            token = data.get('token') or str(uuid4())
            if expire is not None:
                del data['time']
            data['token'] = token
            user_data['data'] = data
            await db.update_user_data(user_id, user_data)
        buttons = [InlineKeyboardButton(text="Refresh Token", url=f'https://t.me/{Config.BOT_NAME}?start={token}')]
        text = "Token is expired, refresh your token and try again." if isExpired else "Your token is valid."
        await message.reply(text=text, reply_markup=InlineKeyboardMarkup([buttons]))
    except Exception as e:
        print(f"An error occurred while generating token: {e}")
