from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import start_kb

from misc import BDB, T

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    start_text = T.StartText
    approve_users = [int(x.strip()) for x in BDB.get_setting("tg_id").split(",")]
    user_id = message.from_user.id
    
    if user_id in approve_users:
        if not BDB.get_user(user_id):
            BDB.add_user(user_id)
        await message.answer(text=start_text, reply_markup=start_kb, disable_web_page_preview=True)
    else:
        await message.answer(text="Цей бот не для тебе, пака 👋")
