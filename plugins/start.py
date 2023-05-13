import random
import os
from pyrogram import Client, filters
from asyncio import sleep
from time import time
from uuid import uuid4
from gif import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from config import Config
from helper.database import db
from helper.token import checking_access

@Client.on_message(filters.command(['start']))
async def start(client, message):
    try:
        if len(message.command) > 1:
            userid = message.from_user.id
            input_token = message.command[1]
            if not await db.is_user_exist(userid):
                return await Config.sendMessage(client, message, 'wait a minute who are you?')
            data = await db.get_user_data(userid)
            if 'token' not in data or data['token'] != input_token:
                return await Config.sendMessage(client, message, 'This is a token already expired')
            await checking_access(userid, message)
            data = await db.get_user_data(userid)
        gifs = os.listdir('./gif')
        selected_gif = random.choice(gifs)
        await message.reply_video(
            video=f'./gif/{selected_gif}',
            caption=f'**Hi There** `',
            supports_streaming=True
        )
    except Exception as e:
        print(f"An error occurred while executing: {e}")
        
@Client.on_message(filters.command(['ping']))
async def ping(client, message):
    start = time()
    await sendMessage(client, message, "😐😑😶")
    end = time()
    duration = round((end - start) * 1000, 3)
    await sendMessage(client, message, f"Ping: {duration}ms")

            
