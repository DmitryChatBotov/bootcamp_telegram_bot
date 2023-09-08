import io
import logging
from datetime import datetime, timedelta
from os import getenv

from aiogram import Bot, F, Router
from aiogram.enums import ContentType
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from common.google_calendar import create_google_calendar_link
from crm_mock.crud.booking import cancel_reservation, create_reservation
from crm_mock.crud.user import get as get_user_from_db
from crm_mock.db import Database
from crm_mock.schemas.booking import Reservation
from crm_mock.schemas.user import User
from crud.conversation import chat_with_llm
from models import whisper_model

router = Router()


class Booking(StatesGroup):
    request = State()
    confirm = State()


class BookingCancel(StatesGroup):
    request = State()
    confirm = State()


def _generate_google_calendar_link_by_booking_result(booking_result) -> str:
    service_date = datetime.strptime(booking_result.date, "%Y-%m-%d").date()
    service_start_time = datetime.strptime(booking_result.time, "%H:%M")
    service_end_time = service_start_time + timedelta(minutes=booking_result.duration)
    service_start_datetime = datetime.combine(service_date, service_start_time.time())
    service_end_datetime = datetime.combine(service_date, service_end_time.time())
    return create_google_calendar_link(
        booking_result.beauty_procedure,
        service_start_datetime,
        service_end_datetime,
    )


@router.message(BookingCancel.request, F.text.lower() == "yes")
async def cancel_booking_handler(message: Message):
    async with Database(getenv("SQLITE_FILE")) as db:
        user: User = await get_user_from_db(db=db, user_id=message.from_user.id)
        try:
            await cancel_reservation(db=db, client_id=user.id)
            await message.answer("Your appointment has been cancelled.")
        except Exception as err:
            logging.error(err)
            await message.answer("Unexpected error, please contact your administrator.")


@router.message(or_f(Booking.request, BookingCancel.request), F.text.lower() == "no")
async def get_administrator(message: Message):
    await message.answer(
        "I am requesting admin support. He'll be here in a few minutes."
    )


@router.message(Booking.request, F.text.lower() == "yes")
async def confirm_booking_handler(message: Message, state: FSMContext):
    agent_result = (await state.get_data()).get("agent_data")
    async with Database(getenv("SQLITE_FILE")) as db:
        user = await get_user_from_db(db=db, user_id=message.from_user.id)
        reservation: Reservation = await create_reservation(
            db=db,
            master_name=agent_result.master_name,
            service_name=agent_result.beauty_service,
            client_name=user.name,
            booking_time=agent_result.booking_time,
            booking_date=agent_result.booking_date,
        )
        if reservation:
            google_calendar_link = _generate_google_calendar_link_by_booking_result(
                reservation
            )
            answer = (
                f"You have reservation: \n"
                f"- {reservation.beauty_procedure}\n"
                f"- Master - {reservation.master if reservation.master else 'Any free master'}\n"
                f"- Date - {reservation.date}\n"
                f"- Time - {reservation.time}\n"
                f"- Price - {reservation.price}\n"
                f"Add [booking]({google_calendar_link}) to google calendar."
            )
            await message.answer(answer, parse_mode="Markdown")
        else:
            await message.answer("Unexpected error, please contact your administrator.")


@router.message(or_f(F.text, F.voice))
async def message_handler(message: Message, state: FSMContext, bot: Bot):
    message_text = ""

    match message.content_type:
        case ContentType.VOICE:
            voice_file_info = await bot.get_file(message.voice.file_id)
            voice_ogg = io.BytesIO()
            await bot.download_file(voice_file_info.file_path, voice_ogg)
            message_text = whisper_model(voice_ogg)
        case ContentType.TEXT:
            message_text = message.text

    action, llm_answer = chat_with_llm(message.from_user.id, message_text)
    match action:
        case "Booking":
            await state.update_data(agent_data=llm_answer)
            match llm_answer.action:
                case "Create":
                    answer = (
                        f"You want to make a reservation: \n"
                        f"- {llm_answer.beauty_service}\n"
                        f"- Master - {llm_answer.master_name if llm_answer.master_name else 'Any free master'}\n"
                        f"- Date - {llm_answer.booking_date}\n"
                        f"- Time - {llm_answer.booking_time} \n"
                        "That is right? Type 'Yes' or 'No'"
                    )
                    await message.answer(answer)
                    await state.set_state(Booking.request)
                case "Cancel":
                    answer = "You want to cancel a reservation.\nThat is right? Type 'Yes' or 'No'"
                    await message.answer(answer)
                    await state.set_state(BookingCancel.request)
        case "Exit":
            await message.answer("We will be glad to see you again!")
        case "Support":
            await message.answer(
                "I am requesting admin support. He'll be here in a few minutes."
            )
        case _:
            await message.answer(llm_answer.text)
