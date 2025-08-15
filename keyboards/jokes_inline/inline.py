from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder

from keyboards import back_to_start_bt

from misc import BDB

jokes_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Гуд муд", callback_data="good_mood")
        ],
        [
            InlineKeyboardButton(text="Щось тарологічне", callback_data="tarological")
        ],
        [
            InlineKeyboardButton(text="Рецепти", callback_data="recipes")
        ],
        [
            InlineKeyboardButton(text="Нагадування", callback_data="reminder")
        ],
        [
            InlineKeyboardButton(text="Підтримка", callback_data="support")
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


async def good_mood_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Цитати", callback_data="quotes"))
    kb.row(InlineKeyboardButton(text="Компліменти", callback_data="compliments"))
    kb.row(InlineKeyboardButton(text="Картинки та меми", callback_data="pictures_memes"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def tarological_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Гороскоп", callback_data="horoscope"))
    kb.row(InlineKeyboardButton(text="Карта Таро дня", callback_data="tarot_card"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def recipes_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Рецепт їжі", callback_data="food_recipe"))
    kb.row(InlineKeyboardButton(text="Рецепт коктейлю", callback_data="cocktail_recipe"))
    kb.row(InlineKeyboardButton(text="Рецепт солодощів", callback_data="sweets_recipe"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def reminder_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Щоденне нагадування", callback_data="daily_reminder"))
    kb.row(InlineKeyboardButton(text="Разове нагадування", callback_data="one_reminder"))
    kb.row(InlineKeyboardButton(text="Планування дня", callback_data="planning_day"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def support_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Терапія", callback_data="therapy"))
    kb.row(InlineKeyboardButton(text="Мотивейшен", callback_data="motivation"))
    kb.row(InlineKeyboardButton(text="Дружня розмова", callback_data="confabulation"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()


async def games_kb(tg_id):
    user = BDB.get_user(tg_id)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Відповідь Так/Ні", callback_data="answer_yes_no"))
    kb.row(InlineKeyboardButton(text="Вікторина", callback_data="quiz"))
    kb.row(InlineKeyboardButton(text="Натисни більше", callback_data="click_more"))
    kb.row(back_to_jokes_bt)

    kb.adjust(1)

    return kb.as_markup()
