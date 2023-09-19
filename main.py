import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.other import other_router
from handlers.admin import admin_router
from handlers.driver import driver_router


async def on_startup():
    pass

async def main():

    bot = Bot(token="5104762167:AAHAXVpkroaiJHpXTQHoEmmLpzzPOzPzqwI", parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # initialize routers
    dp.include_router(other_router)
    dp.include_router(admin_router)
    dp.include_router(driver_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(name)s: %(message)s")
    asyncio.run(main())


