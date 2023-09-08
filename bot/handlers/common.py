from os import getenv

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from crm_mock.crud.user import get as get_user_from_db
from crm_mock.db import Database

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    """Send start message to bot."""

    async with Database(getenv("SQLITE_FILE")) as db:
        if await get_user_from_db(db=db, user_id=message.from_user.id):
            await message.answer(
                "Hello! Welcome to Krasota.Hamburg studio. Glad to see you again!"
            )
        else:
            button = KeyboardButton(text="Share contact", request_contact=True)
            keyword = ReplyKeyboardMarkup(keyboard=[[button]])
            await message.answer(
                "Hello! Welcome to Krasota.Hamburg studio. To continue working, please register.",
                reply_markup=keyword,
            )
