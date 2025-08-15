from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "shop")
async def shop_call(callback_query: CallbackQuery):
    pass
