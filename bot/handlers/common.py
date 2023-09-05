from os import getenv

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from crud.user import get_user

from db import Database

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    async with Database(getenv("SQLITE_FILE")) as db:
        if await get_user(db, message.from_user.id):
            await message.answer(
                "Здравствуйте! Вас приветствует студия Krasota.Hamburg. Рады снова вас видеть!"
            )
        else:
            button = KeyboardButton(text="Share contact", request_contact=True)
            keyword = ReplyKeyboardMarkup(keyboard=[[button]])
            await message.answer(
                "Здравствуйте! Вас приветствует студия Krasota.Hamburg. Чтобы продолжить работу, пожалуйста, зарегистрируйтесь",
                reply_markup=keyword,
            )
