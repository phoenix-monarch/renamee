import os, random, asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaAnimation, InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from helper.token import none_admin_utils
from time import time
from uuid import uuid4
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard
from helper.knockers import handle_callback

page_number = [0]

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    try:
        userid = message.from_user.id
        data = await db.get_user_data(userid)
        input_token = None
        if len(message.command) > 1:
            input_token = message.command[1]
        if not await db.is_user_exist(userid):
            gif_url = 'https://graph.org/file/a58b959cc11443ac4e70b.mp4'
            caption = 'Who are you?'
            await message.reply_video(
                video=gif_url,
                caption=caption,
                supports_streaming=True
            )
            return
 
        if 'token' not in data or data['token'] != input_token:
            gif_url = 'https://graph.org/file/f6e6beb62a16a46642fb4.mp4'
            caption = '''This token is already expired.
1. After updating the token if you use /start again, you will get this message.
2. Don't worry because other functions will work.
3. Only refresh the token after 24 hours using the /ping command. I will fix this soon.'''
            await message.reply_video(
                video=gif_url,
                caption=caption,
                supports_streaming=True
            )
            return
        
        data['token'] = str(uuid4())
        data['time'] = time()
        await db.update_user_data(userid, data)

        caption = get_page_caption(page_number[0], message.from_user.first_name, message.from_user.last_name, None if not message.from_user.username else '@' + message.from_user.username, message.from_user.mention, message.from_user.id)
        inline_keyboard = get_inline_keyboard(page_number[0])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await message.reply_video(
            video=get_page_gif(page_number[0]),
            caption=caption,
            supports_streaming=True,
            reply_markup=reply_markup
        )
        
    except Exception as e:
        print(f"An error occurred while executing start: {e}")

@Client.on_callback_query()
async def callback_query(client, callback_query):
    try:
        await handle_callback(callback_query, page_number)
    except Exception as e:
        print(f"An error occurred while handling callback in start query: {e}")
