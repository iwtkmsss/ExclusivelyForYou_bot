from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder

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

async def paginatios_kb(page: int, max_page: int):
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text=(("◀️" if page >= 1 else "❌") + " Попередня"),
                             callback_data=f"page:{page - 1}" if page >= 1 else "noop"),
        InlineKeyboardButton(text=("Наступна " + ("❌" if page >= max_page else "▶️")),
                             callback_data="noop" if page >= max_page else f"page:{page + 1}")
        )
    
    return kb

