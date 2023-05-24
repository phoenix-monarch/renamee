from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAnimation, InputMediaVideo
from helper.bossoms import get_page_caption, get_inline_keyboard, get_page_gif 

async def handle_callback(client, query: CallbackQuery):
    data = query.data

    if data == "previous":
        if page_number[0] == 0:
            page_number[0] = 0
        else:
            page_number[0] -= 1
    elif data == "next":
        if page_number[0] == 4:
            page_number[0] = 4
        else:
            page_number[0] += 1

    caption = get_page_caption(page_number, query.from_user.first_name, query.from_user.last_name, None if not query.from_user.username else '@' + query.from_user.username, query.from_user.mention, query.from_user.id)
    inline_keyboard = get_inline_keyboard(page_number)

    try:
        if isinstance(query.message.media, (InputMediaVideo, InputMediaAnimation)):
            video_path = get_page_gif(page_number)
            video = InputMediaVideo(media=video_path, caption=caption)
            await query.message.edit_media(
                media=video
            )
        if query.message.caption != caption or query.message.reply_markup != InlineKeyboardMarkup(inline_keyboard):
            await query.message.edit_caption(
                caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
            
    except Exception as e:
        print(f"An error occurred in handle_callback: {e}")
