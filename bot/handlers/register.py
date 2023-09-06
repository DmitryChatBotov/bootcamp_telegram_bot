import logging
from os import getenv

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove

from crud.user import register_user
from db import Database, get_db
from schemas.user import User

router = Router()


@router.message(F.contact)
async def register_user(message: Message) -> None:
    """Register user in db by sharing contact."""
    contact = message.contact
    phone_number = contact.phone_number
    user_id = message.from_user.id
    name = f"{contact.first_name} {contact.last_name}"
    user = User(user_id=user_id, phone=phone_number, name=name)
    try:
        async with Database(getenv("SQLITE_FILE")) as db:
            await register_user(db, user)

        await message.answer(
            f"Thank you for sharing your contact information!\n"
            f"Phone number: {phone_number}\n"
            f"Name: {name}\n",
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as err:
        logging.error(err)
        await message.answer(
            "User registration failed, please try again later."
        )
