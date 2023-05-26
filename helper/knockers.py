from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAnimation, InputMediaVideo
from helper.bossoms import get_page_caption, get_inline_keyboard, get_page_gif 

async def handle_callback(callback_query: CallbackQuery, page_number, user: User):
    data = callback_query.data

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

    caption = get_page_caption(page_number[0], user.first_name, user.last_name, user.username, user.mention, user.id)
    inline_keyboard = get_inline_keyboard(page_number[0])

    try:
        if isinstance(callback_query.message.media, (InputMediaVideo, InputMediaAnimation)):
            video_path = get_page_gif(page_number[0])
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
