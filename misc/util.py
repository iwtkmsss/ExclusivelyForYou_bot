import asyncio
from aiogram.types import Message


async def loading_message(message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    
    msg = await message.answer("Loading...")

    return msg
