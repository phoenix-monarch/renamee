import random
import time 
from uuid import uuid4
from time import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery
from helper.database import db
from config import Config, Txt

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        user = message.from_user
        await db.add_user(client, message)
        data = await db.get_user_data(user.id)
        if 'token' not in data[user.id]:
               return await message.reply(text='User not found.')
        if len(message.command) > 1:
            input_token = message.command[1].upper()
            if data[user.id]['token'] != input_token:
                return await message.reply(text='Invalid token.')
        data[user.id]['token'] = str(uuid4())
        data[user.id]['time'] = int(time.time())
        await db.update_user_data(user.id, data)
        button = InlineKeyboardMarkup([[
            InlineKeyboardButton("👨‍💻 Dᴇᴠꜱ 👨‍💻", callback_data='dev')
        ],[
            InlineKeyboardButton('📯 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/kirigayaakash'),
            InlineKeyboardButton('💁‍♂️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/kirigaya_asuna')
        ],[
            InlineKeyboardButton('🎛️ Aʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('🛠️ Hᴇʟᴩ', callback_data='help')
        ]])
        if Config.START_PIC:
            await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
        else:
            await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)
    except Exception as e:
        print(f"An error occurred while executing: {e}")


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("👨‍💻 Dᴇᴠꜱ 👨‍💻", callback_data='dev')
                ],[
                InlineKeyboardButton('📯 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/kirigayaakash'),
                InlineKeyboardButton('💁‍♂️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/kirigaya_asuna')
                ],[
                InlineKeyboardButton('🎛️ Aʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('🛠️ Hᴇʟᴩ', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://t.me/kirigayaakash/1063")
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://t.me/kirigayaakash/1063")
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])            
        )
    elif data == "dev":
        await query.message.edit_text(
            text=Txt.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://t.me/kirigayaakash/1063")
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
            
