import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from helper.database import db
from helper.token import none_admin_utils

@Client.on_message(filters.private & filters.command('ping'))
async def ping(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
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
    except AttributeError:
        print("The 'message.chat' object is None or doesn't have the 'write' attribute.")
    except Exception as e:
        print(f"An error occurred while executing ping: {e}")


@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return
        if len(message.command) == 1:
            return await message.reply_text("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`**")
        caption = message.text.split(" ", 1)[1]
        await db.set_caption(message.from_user.id, caption=caption)
        await message.reply_text("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")
    except Exception as e:
        print(f"An error occurred while executing set_caption: {e}")

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return
        caption = await db.get_caption(message.from_user.id)
        if not caption:
            return await message.reply_text("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
        await db.set_caption(message.from_user.id, caption=None)
        await message.reply_text("__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__")
    except Exception as e:
        print(f"An error occurred while executing del_caption: {e}")

@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return	
        caption = await db.get_caption(message.from_user.id)
        if caption:
            await message.reply_text(f"**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`")
        else:
            await message.reply_text("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    except Exception as e:
        print(f"An error occurred while executing see_caption: {e}")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return
        thumb = await db.get_thumbnail(message.from_user.id)
        if thumb:
            await client.send_photo(chat_id=message.chat.id, photo=thumb)
        else:
            await message.reply_text("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")
    except Exception as e:
        print(f"An error occurred while executing viewthumb: {e}")

@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
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
        await db.set_thumbnail(message.from_user.id, file_id=None)
        await message.reply_text("❌️ Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ")
    except Exception as e:
        print(f"An error occurred while executing removethumb: {e}")        

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    try:
        none_admin_msg, error_button = await none_admin_utils(message)
        error_msg = []
        if none_admin_msg:
            error_msg.extend(none_admin_msg)
            await message.reply_text(
                text='\n'.join(error_msg),
                reply_markup=InlineKeyboardMarkup([[error_button]])
            )
            return
        mkn = await message.reply_text("Please Wait ...")
        await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)
        await mkn.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")
    except Exception as e:
        print(f"An error occurred while executing addthumbs: {e}")
