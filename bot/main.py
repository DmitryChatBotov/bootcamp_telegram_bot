import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
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


@dp.message(F.voice)
async def voice_message_handler(message: types.Message):
    await message.reply_voice(message.voice.file_id)


@dp.message(F.text)
async def text_message_handler(message: types.Message):
    await message.reply(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
