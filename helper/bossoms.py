import os, random
from gif import *
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_page_gif(page_number):
    gifs = os.listdir('./gif')
    selected_gif = random.choice(gifs)
    gif_path = selected_gif
    return f'./gif/{gif_path}'

def get_page_caption(page_number, first_name):
    if page_number == 0:
        page_text = Config.Text
    elif page_number == 1:
        page_text = Config.Text1
    elif page_number == 2:
        page_text = Config.Text2
    elif page_number == 3:
        page_text = Config.Text3
    elif page_number == 4:
        page_text = Config.Text4

    return f"Hello {first_name}!\n\n{page_text}"

def get_inline_keyboard(page_number):
    inline_keyboard = []

    if page_number > 0:
        inline_keyboard.append(
            [InlineKeyboardButton("👈", callback_data="previous")]
        )
    if page_number < 4:
        inline_keyboard.append(
            [InlineKeyboardButton("👉", callback_data="next")]
        )

    return [inline_keyboard]
