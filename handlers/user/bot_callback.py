from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import start_kb, jokes_kb

router = Router()


@router.callback_query(F.data == "back_to_start")
async def shop_call(callback_query: CallbackQuery):
    start_text = "START TEXT"

    await callback_query.message.edit_text(text=start_text, reply_markup=start_kb)


@router.callback_query(F.data == "back_to_jokes")
async def back_to_jokes_call(callback_query: CallbackQuery):
    text = "JOKES TEXT"

    await callback_query.message.edit_text(text=text,
                                           reply_markup=jokes_kb)
