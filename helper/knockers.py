from pyrogram.types import InputMediaVideo, InputMediaAnimation, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard

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

    caption = get_page_caption(current_page[0], callback_query.from_user.first_name)
    inline_keyboard = get_inline_keyboard(current_page[0])

    try:
        edit_video = not callback_query.message.video

        if edit_video:
            video_path = get_page_gif(current_page[0])
            video = InputMediaVideo(media=video_path, caption=caption)
            await callback_query.message.edit_media(
                media=video,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
        else:
            await callback_query.message.edit_caption(caption)
            await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard))
    except Exception as e:
        print(f"An error occurred in handle_callback: {e}")
