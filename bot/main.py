import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from bestconfig import Config

config = Config()
API_TOKEN = config.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def send_welcome_message(message: types.Message) -> None:
    await message.answer("Hello, sweetie!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
