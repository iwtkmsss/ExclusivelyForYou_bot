from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "character")
async def character_call(callback_query: CallbackQuery):
    pass
