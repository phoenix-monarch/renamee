import os, random, asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaAnimation, InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from helper.token import none_admin_utils
from time import time
from uuid import uuid4
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard
from helper.knockers import handle_callback

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
        
        print("Before update_user_data")
        data['token'] = str(uuid4())
        data['time'] = time()
        print("Inside db.update_user_data")
        await db.update_user_data(userid, data)
        print("After update_user_data")

        print("Before page_number")
        page_number = 0
        print("Before caption")
        caption = get_page_caption(page_number, message.from_user.first_name)
        print("Before inline_keyboard")
        inline_keyboard = get_inline_keyboard(page_number)
        print("Before message.reply_video")
        await message.reply_video(
            video=get_page_gif(page_number),
            caption=caption,
            supports_streaming=True,
            reply_markup=InlineKeyboardMarkup(inline_keyboard)
        )
        print("After reply_video")    
    except Exception as e:
        print(f"An error occurred while executing start: {e}")

@Client.on_callback_query()
async def callback_query(client, callback_query):
    try:
        await handle_callback(callback_query)
    except Exception as e:
        print(f"An error occurred while handling callback query: {e}")

@Client.on_message(filters.private & filters.command(['ping']))
async def ping(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await client.send_message(
                chat_id=message.chat.id,
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return

        start = time()
        sent_message = await message.reply("😐😑😶")
        await asyncio.sleep(3)
        end = time()
        duration = round((end - start) * 1000, 3)
        await sent_message.edit_text(f"😶😑😏: {duration}ms")
    except Exception as e:
        print(f"An error occurred while executing ping: {e}")
