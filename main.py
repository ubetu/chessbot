import asyncio
import logging
from bot_creating import bot, dp
from handlers import router_main, router_connection, router_playing
async def main():
    dp.include_routers(router_main, router_connection, router_playing)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
