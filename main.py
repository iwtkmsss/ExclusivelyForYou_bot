import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.user import bot_callback, bot_messages, start_command
from handlers.user.start_menu import jokes_call, shop_call, character_call
from handlers.admin import command
from misc import TOKEN, BDB


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start_command.router,
        command.router,
        bot_callback.router,
        bot_messages.router,
        jokes_call.router,
        shop_call.router,
        character_call.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("[+] BOT STARTING")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[-] BOT HAS BEEN DISABLE")
        BDB.close()
