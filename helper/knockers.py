from pyrogram.types import InputMediaVideo, InputMediaAnimation, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard

async def handle_callback(callback_query: CallbackQuery, current_page):
    data = callback_query.data

    if data == "previous":
        current_page -= 1
    elif data == "next":
        current_page += 1

    print(f"Current page: {current_page}")

    caption = get_page_caption(current_page, callback_query.from_user.first_name)
    inline_keyboard = get_inline_keyboard(current_page)

    print(f"Caption: {caption}")
    print(f"Inline keyboard: {inline_keyboard}")

    try:
        edit_video = not callback_query.message.video

        if edit_video:
            video_path = get_page_gif(current_page)
            video = InputMediaVideo(media=video_path, caption=caption)
            print(f"Editing media: {video_path}")
            await callback_query.message.edit_media(
                media=video,
                reply_markup=InlineKeyboardMarkup(inline_keyboard)
            )
        else:
            await callback_query.message.edit_caption(caption)
            await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard))
    except Exception as e:
        print(f"An error occurred: {e}")
