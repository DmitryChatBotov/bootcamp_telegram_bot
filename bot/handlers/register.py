import logging
from os import getenv

from aiogram import F, Router
from aiogram.types import Contact, Message, ReplyKeyboardRemove

from crm_mock.crud.user import register
from crm_mock.db import Database, get_db
from crm_mock.schemas.user import User

router = Router()


@router.message(F.contact)
async def register_user(message: Message) -> None:
    """Register user in database by sharing contact's info."""
    contact: Contact = message.contact
    phone_number: str = contact.phone_number
    user_id: int = message.from_user.id
    name: str = f"{contact.first_name}"
    if contact.last_name:
        name += f" {contact.last_name}"
    user: User = User(id=user_id, phone=phone_number, name=name)
    try:
        async with Database(getenv("SQLITE_FILE")) as db:
            await register(db=db, user=user)
        answer = (
            f"Thank you for sharing your contact information!\n"
            f"Phone number: {phone_number}\n"
            f"Name: {name}\n"
        )
        await message.answer(
            answer,
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as err:
        logging.error(err)
        await message.answer("User registration failed, please try again later.")
