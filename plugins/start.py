import os, random, asyncio
from gif import *
from config import Config
from pyrogram import Client, filters
from pyrogram.types import InputMediaAnimation, InlineKeyboardMarkup
from helper.database import db
from helper.token import none_admin_utils
from time import time

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
            caption = 'This is a token already expired'
            await message.reply_video(
                video=gif_url,
                caption=caption,
                supports_streaming=True
            )
            return

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

        data['token'] = input_token
        data['time'] = time()
        await db.update_user_data(userid, data)
        
        gifs = os.listdir('./gif')
        selected_gif = random.choice(gifs)
        caption = f'Hello {message.from_user.first_name}! Welcome to the bot'
        await message.reply_video(
            video=f'./gif/{selected_gif}',
            caption=caption,
            supports_streaming=True
        )
    except Exception as e:
        print(f"An error occurred while executing start: {e}")

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
