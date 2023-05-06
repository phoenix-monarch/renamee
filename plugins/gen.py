from config import Config
from helper.database import db
from time import time
from uuid import uuid4
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shortener import shorten_url

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
            url = f'https://t.me/{Config.BOT_NAME}?start={token}'
            shortened_url = shorten_url(url)  # pass the generated URL to the `shorten_url` function
            text = "Token is expired, refresh your token and try again." if isExpired else "Your token is valid."
        await message.reply(text=text, reply_markup=InlineKeyboardMarkup([buttons, [InlineKeyboardButton(text="Shortened URL", url=shortened_url)]])) # add a button with the shortened URL to the inline keyboard
    except Exception as e:
        print(f"An error occurred while generating token: {e}")
