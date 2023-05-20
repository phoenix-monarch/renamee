from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from helper.bossoms import get_page_gif, get_page_caption, get_inline_keyboard

async def handle_callback(callback_query: CallbackQuery):
    page_number = 0
    data = callback_query.data
    if data == "previous":
        page_number = max(page_number - 1, 0)
    elif data == "next":
        page_number = min(page_number + 1, 4)

    caption = get_page_caption(page_number, callback_query.from_user.first_name)
    inline_keyboard = get_inline_keyboard(page_number)

    await callback_query.edit_message_media(
        media=get_page_gif(page_number),
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
    )
