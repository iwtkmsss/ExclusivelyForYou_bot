from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder

from keyboards import back_to_start_bt, paginatios_kb

from misc import BDB, get_status_category, t_zodiac_signs

jokes_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="😌 Гуд муд", callback_data="good_mood")
        ],
        [
            InlineKeyboardButton(text="🔮 Щось тарологічне", callback_data="tarological")
        ],
        [
            InlineKeyboardButton(text="📖 Рецепти", callback_data="recipes")
        ],
        [
            InlineKeyboardButton(text="⏰ Нагадування", callback_data="reminder")
        ],
        [
            InlineKeyboardButton(text="🤝 Підтримка", callback_data="support")
        ],
        [
            InlineKeyboardButton(text="🎮 Ігри", callback_data="games")
        ],
        [
            back_to_start_bt
        ]
    ]
)

back_to_jokes_bt = InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_jokes")


async def good_mood_kb(tg_id: int):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🧐 Цитати", callback_data="quotes"))
    kb.row(InlineKeyboardButton(text="🤩 Компліменти", callback_data="compliments"))
    kb.row(InlineKeyboardButton(text="😂 Картинки та меми", callback_data="pictures_memes"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def tarological_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✨ Гороскоп", callback_data="horoscope"))
    kb.row(InlineKeyboardButton(text="🔯 Матриця долі", callback_data="matrix_destiny"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def recipes_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="👑 Преміум рецепти", callback_data="premium_recipes"))
    kb.row(InlineKeyboardButton(text="🧑‍🍳 Рецепт їжі", callback_data="food_recipe"))
    kb.row(InlineKeyboardButton(text="🍹 Рецепт коктейлю", callback_data="cocktail_recipe"))
    kb.row(InlineKeyboardButton(text="🍮 Рецепт солодощів", callback_data="sweets_recipe"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


translate_world = {
    "breakfasts": "Cніданки",
    "dinners": "Вечері",
    "dishes": "Страви",
    "salads": "Салати"
}
async def premium_recipes_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    status_category = await get_status_category()
    for s in status_category.keys():
        kb.row(InlineKeyboardButton(text=f"👑 {translate_world[s]} - {len(status_category[s])}",
                                    callback_data=f"recipe_{s}" if len(status_category[s]) > 0 else "no_action"))
    kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_recipes"))

    kb.adjust(1)

    return kb.as_markup()


back_to_premium_recipes_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_premium_recipes")
        ]
    ]
)


async def food_recipe_kb(page: int, max_page: int):
    paginations_kb = await paginatios_kb(page, max_page)

    paginations_kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_recipes"))

    return paginations_kb.as_markup()


async def reminder_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🔔 Щоденне нагадування", callback_data="daily_reminder"))
    kb.row(InlineKeyboardButton(text="📅 Разове нагадування", callback_data="one_reminder"))
    kb.row(InlineKeyboardButton(text="📈 Планування дня", callback_data="planning_day"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def support_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🧠 Терапія", callback_data="therapy"))
    kb.row(InlineKeyboardButton(text="🏆 Мотивейшен", callback_data="motivation"))
    kb.row(InlineKeyboardButton(text="☕ Дружня розмова", callback_data="confabulation"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def games_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🧐 Відповідь Так/Ні", callback_data="answer_yes_no"))
    kb.row(InlineKeyboardButton(text="🤔 Вікторина", callback_data="quiz"))
    kb.row(InlineKeyboardButton(text="👇 Натисни більше", callback_data="click_more"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


back_to_tarological_bt = InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_tarological")

async def all_horoscope_kb():
    kb = InlineKeyboardBuilder()

    for zodiac_sing in t_zodiac_signs.keys():
        text = t_zodiac_signs[zodiac_sing]["sign"] + " " + t_zodiac_signs[zodiac_sing]["name"]
        kb.row(InlineKeyboardButton(text=text, callback_data=f"zodiac_{zodiac_sing}"))

    kb.adjust(2)

    kb.row(back_to_tarological_bt)

    return kb.as_markup()


back_to_all_horoscope_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_all_horoscope")
        ]
    ]
)


async def matrix_destiny_kb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="👩🏽 Персональна", callback_data="matrix_destiny_personal"))
    kb.row(InlineKeyboardButton(text="👫 Сумісність", callback_data="matrix_destiny_compatibility"))
    kb.row(back_to_tarological_bt)

    return kb.as_markup()


back_to_m_d_personal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_m_d_personal")
        ]
    ]
)


async def matrix_destiny_personal_kb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="👨🏻‍💼 Чоловік", callback_data="m_d_personal_man"))
    kb.row(InlineKeyboardButton(text="👩🏽‍💼 Жінка", callback_data="m_d_personal_woman"))
    kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_matrix_destiny"))

    return kb.as_markup()


async def matrix_paginatios_kb(page: int, max_page: int):
    paginations_kb = await paginatios_kb(page, max_page)

    paginations_kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_m_d_personal"))

    return paginations_kb.as_markup()
