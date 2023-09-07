import logging
from os import getenv

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from crud.user import get_user
from db import Database

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    """Send start message to bot."""

    async with Database(getenv("SQLITE_FILE")) as db:
        user = await get_user(db, message.from_user.id)
        logging.info(f"user: {user}")
        if await get_user(db, message.from_user.id):
            await message.answer(
                "Hello! Welcome to Krasota.Hamburg studio. Glad to see you again!"
            )
        else:
            button = KeyboardButton(text="Share contact", request_contact=True)
            keyword = ReplyKeyboardMarkup(keyboard=[[button]])
            await message.answer(
                "Hello! Welcome to Krasota.Hamburg studio. To continue working, please register",
                reply_markup=keyword,
            )
