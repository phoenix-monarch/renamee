import random, os, asyncio, time
from pyrogram import Client, filters
from gif import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from helper.database import db
from config import Config 
from helper.token import validate_user
 
@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    try:
        is_valid = await validate_user(client, message)
        if not is_valid:
            return
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
        is_valid = await validate_user(client, message)
        if not is_valid:
            return
        start = time()
        sent_message = await message.reply("😐😑😶")
        await asyncio.sleep(3)
        end = time()
        duration = round((end - start) * 1000, 3)
        await sent_message.edit_text(f"😶😑😏: {duration}ms")
    except Exception as e:
        print(f"An error occurred while executing ping: {e}")
