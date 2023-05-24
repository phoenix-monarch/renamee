import os, random, asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaAnimation, InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from helper.token import none_admin_utils
from time import time
from uuid import uuid4
from gif import *
from config import Config, Txt

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

        button = InlineKeyboardMarkup([[
            InlineKeyboardButton("👨‍💻 Dᴇᴠꜱ 👨‍💻", url='tg://settings')
        ], [
            InlineKeyboardButton('📯 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/kirigayaakash'),
            InlineKeyboardButton('💁‍♂️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/kirigaya_asuna')
        ], [
            InlineKeyboardButton('🛠️ Hᴇʟᴩ', callback_data='help')
        ]])

        gifs = os.listdir('./gif')
        selected_gif = random.choice(gifs)
        caption = '''Hello {message.from_user.mention}!

1. 🙏 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚃𝚘 𝚃𝚑𝚎 𝙱𝚘𝚝.!
2. 👋 𝚂𝚒𝚗𝚌𝚎 𝚈𝚘𝚞 𝚂𝚝𝚊𝚛𝚝𝚎𝚍 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙸 𝙷𝚘𝚙𝚎 𝚈𝚘𝚞 𝙰𝚕𝚕 𝙺𝚗𝚘𝚠 𝚆𝚑𝚊𝚝 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙳𝚘.......𝙸𝚏 𝙽𝚘𝚝 𝙰 𝙱𝚛𝚒𝚎𝚏 𝙽𝚘𝚝𝚎.....
3. ✍ 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙲𝚊𝚗 𝚁𝚎𝚗𝚊𝚖𝚎 𝙵𝚒𝚕𝚎𝚜.
4. 🧑‍💻 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙲𝚘𝚛𝚎 𝚁𝚎𝚙𝚘 𝙸𝚜 𝙿𝚢𝚛𝚘 𝙱𝚘𝚝𝚣 𝚁𝚎𝚙𝚘 𝙱𝚞𝚝 𝙸 𝙷𝚊𝚟𝚎 𝙴𝚍𝚒𝚝𝚎𝚍 𝚃𝚑𝚎 𝙱𝚘𝚝  𝚁𝚎𝚙𝚘 𝙵𝚘𝚛 𝙼𝚢 𝙿𝚞𝚛𝚙𝚘𝚜𝚎.
5. 🤝 𝙸𝚏 𝚈𝚘𝚞 𝚆𝚒𝚜𝚑 𝚃𝚘 𝚄𝚜𝚎 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 . 𝚈𝚘𝚞 𝙲𝚊𝚗 𝚄𝚜𝚎 𝙸𝚝.'''
        await message.reply_video(
            video=f'./gif/{selected_gif}',
            caption=caption,
            reply_markup=button,
            disable_web_page_preview=True,
            supports_streaming=True
        )
    except Exception as e:
        print(f"An error occurred while executing start: {e}")


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "help":
        await query.message.edit_caption(
            caption=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close")
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
