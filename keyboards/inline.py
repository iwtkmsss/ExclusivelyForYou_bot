from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

back_to_start_bt = InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👩🏽 Персонаж", callback_data="character")
        ],
        [
            InlineKeyboardButton(text="🙃 Приколяхи", callback_data="jokes")
        ],
        [
            InlineKeyboardButton(text="🛍 Магазин", callback_data="shop")
        ]
    ]
)
