from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAnimation, InputMediaVideo
from helper.bossoms import get_page_caption, get_inline_keyboard, get_page_gif 

async def handle_callback(callback_query: CallbackQuery, current_page):
    data = callback_query.data

    if data == "previous":
        if current_page[0] == 0:
            current_page[0] = 0
        else:
            current_page[0] -= 1
    elif data == "next":
        if current_page[0] == 4:
            current_page[0] = 4
        else:
            current_page[0] += 1

    caption = get_page_caption(page_number, callback_query.from_user.first_name, callback_query.from_user.last_name, None if not callback_query.from_user.username else '@' + callback_query.from_user.username, callback_query.from_user.mention, callback_query.from_user.id)
    inline_keyboard = get_inline_keyboard(current_page[0])

    try:
        if isinstance(callback_query.message.media, (InputMediaVideo, InputMediaAnimation)):
            video_path = get_page_gif(current_page[0])
            video = InputMediaVideo(media=video_path, caption=caption)
            await callback_query.message.edit_media(
                media=video
            )
        if callback_query.message.caption != caption or callback_query.message.reply_markup != InlineKeyboardMarkup(inline_keyboard):
            await callback_query.message.edit_caption(
                caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
            
    except Exception as e:
        print(f"An error occurred in handle_callback: {e}")
