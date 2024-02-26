import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import bot_creating
import config
from handlers import router_main

async def main():
    bot = bot_creating.bot
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router_main)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
