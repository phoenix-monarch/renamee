from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db
from time import time
from uuid import uuid4
from shortener import shorten_url


async def checking_access(user_id, user_data):
    if not Config.TOKEN_TIMEOUT:
        return None, None
    user = await db.col.find_one({'_id': int(user_id)})
    if user is None:
        return 'User not found in the database', None
    expire = user_data.get('time')
    is_expired = (expire is None or (expire is not None and (time() - expire) > Config.TOKEN_TIMEOUT))
    if is_expired:
        token = user_data.get('token') if (expire is None and 'token' in user_data) else str(uuid4())
        if expire is not None:
            await db.update_user_data(user_id, {'time': None})
        await db.update_user_data(user_id, {'token': token})
        if user_data.get('time') is None:
            user_data.pop('time')
        if user_data.get('token') is None:
            user_data.pop('token')
        await db.update_user_data(user_id, user_data)
        url = f'https://t.me/{Config.BOT_NAME}?start={token}'
        shortened_url = shorten_url(url)  # pass the generated URL to the shorten_url function
        text = "🤣Here is your wedding ring🤣:"
        await message.reply(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Start bot", url=shortened_url)],
            ])
        ) # add a button with the shortened URL to the inline keyboard
    else:
        return None, None


async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.FORCE_SUB:
        return False
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return True
        else:
            return False
    except UserNotParticipant:
        pass
    return True


@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    # Check if user token is expired or not
    error_message, user_data = await checking_access(message.from_user.id, await db.get_user_data(message.from_user.id))
    if error_message is not None:
        return await message.reply_text(error_message)

    # If token is expired, restrict bot's access until a new token is set
    while user_data.get('time') is not None and (time() - user_data.get('time')) > Config.TOKEN_TIMEOUT:
        await message.reply_text('Your token has expired. Please set a new token to continue.')
        await checking_access(message.from_user.id, await db.get_user_data(message.from_user.id))
        user_data = await db.get_user_data(message.from_user.id)
    
    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=f"https://t.me/{Config.FORCE_SUB}")]]
    text = "**Sorry Dude, you're not joined my channel 😐. So please join our update channel to continue.**"
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return await client.send_message(message.from_user.id, text="Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")  
    except UserNotParticipant:                       
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
           
