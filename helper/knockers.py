from pyrogram.types import InputMediaVideo, InputMediaAnimation, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard

async def handle_callback(callback_query: CallbackQuery):
    page_number = 0
    data = callback_query.data
    if data == "previous":
        page_number -= 1
    elif data == "next":
        page_number += 1

    caption = get_page_caption(page_number, callback_query.from_user.first_name)
    inline_keyboard = get_inline_keyboard(page_number)

    try:
        video = callback_query.message.video
        if not video:
            video_path = get_page_gif(page_number)
            video = InputMediaVideo(media=video_path)
            await callback_query.message.edit_media(
                media=video,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
        else:
            await callback_query.edit_message_caption(caption)
            await callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard))
    except Exception as e:
        print(f"An error occurred: {e}")
