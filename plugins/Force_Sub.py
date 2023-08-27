from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.FORCE_SUB:
        return False
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        if user.status == "kicked":
            return True
        elif user.status == "restricted":
            return False           
        else:
            return False
    except UserNotParticipant:
        return True

@Client.on_message(filters.private & filters.create(not_subscribed))
async def force_sub(client, message):
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        if not link:
            await client.export_chat_invite_link(Config.FORCE_SUB)
            link = (await user.chat.get_invite_link()).invite_link
        invitelink = link
        if user.status == "kicked":
            await client.send_message(message.from_user.id, text="Sorry, You're Banned To Use Me")
            return
    except UserNotParticipant:
        pass

    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=invitelink)]]
    text = "**Sorry Dude, You're Not Joined My Channel 😐. So Please Join Our Update Channel To Continue**"
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
