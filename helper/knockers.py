from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAnimation, InputMediaVideo
from helper.bossoms import get_page_caption, get_inline_keyboard, get_page_gif 

async def handle_callback(callback_query: CallbackQuery, current_page):
    data = callback_query.data

    print("Received callback data:", data)

    if data == "previous":
        if current_page[0] == 0:
            current_page[0] = 0
        else:
            current_page[0] -= 1
        print("Previous button clicked. Current page:", current_page[0])
    elif data == "next":
        if current_page[0] == 4:
            current_page[0] < 4
        else:
            current_page[0] += 1
        print("Next button clicked. Current page:", current_page[0])
        print("Debug: Inside 'next' section")

    caption = get_page_caption(current_page[0], callback_query.from_user.first_name)
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
            print("Caption and reply markup edited. Caption:", caption)
    except Exception as e:
        print(f"An error occurred in handle_callback: {e}")
