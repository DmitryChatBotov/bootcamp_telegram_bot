import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, register, user_request


async def main():
    logging.basicConfig(
        level=logging.INFO,


        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # await create_database()
    # await fill_db_with_temp_data()

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(getenv("TELEGRAM_BOT_TOKEN"))

    dp.include_router(common.router)
    dp.include_router(user_request.router)
    dp.include_router(register.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
