import io

import logging
from os import getenv
import pytz
from aiogram import Bot, F, Router
from aiogram.types import Message
from datetime import datetime, timedelta
from common.google_calendar import create_google_calendar_link
from crud.booking import booking, cancel_booking
from crud.conversation import chat_with_llm
from crud.user import get_user
from db import Database
from models import whisper_model

router = Router()

EDT = pytz.timezone('Asia/Yekaterinburg')


@router.message(F.voice)
async def voice_message_handler(message: Message, bot: Bot):
    voice_file_info = await bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    transription = whisper_model(voice_ogg)
    llm_answer = chat_with_llm(message.from_user.id, transription)
    await message.answer(llm_answer["output"])


@router.message(F.text)
async def text_message_handler(message: Message):
    llm_answer = chat_with_llm(message.from_user.id, message.text)
    agent_result = llm_answer.get("intermediate_steps")[-1][-1]
    if isinstance(agent_result, dict):
        async with Database(getenv("SQLITE_FILE")) as db:
            user = await get_user(db, message.from_user.id)
            match agent_result.get("action"):
                case "Create":
                    booking_result = await booking(
                        db=db,
                        master_name=agent_result.get("master_name", None),
                        service_name=agent_result.get("beauty_service"),
                        client_name=user.get("name"),
                        booking_time=agent_result.get("booking_time"),
                        booking_date=agent_result.get("booking_date"),
                    )
                    if booking_result:
                        service_date = datetime.strptime(booking_result.get('date'), "%Y-%m-%d").date()
                        service_start_time = datetime.strptime(booking_result.get('time'), "%H:%M")
                        service_end_time = service_start_time + timedelta(minutes=booking_result.get('duration'))
                        service_start_datetime = datetime.combine(service_date, service_start_time.time())
                        service_end_datetime = datetime.combine(service_date, service_end_time.time())
                        google_calendar_link = create_google_calendar_link(booking_result.get('service_name'),
                                                                           service_start_datetime, service_end_datetime)
                        logging.info(google_calendar_link)
                        template = f"You have been enrolled to the master {booking_result.get('master_name')}. Date: {booking_result.get('date')}. Time: {booking_result.get('time')}. Service: {booking_result.get('service_name')}. Price: {booking_result.get('price')}. Add [booking]({google_calendar_link}) to google calendar"
                        await message.answer(template, parse_mode="Markdown")
                    else:
                        await message.answer(
                            "Unexpected error, please contact your administrator"
                        )
                case "Cancel":
                    booking_result = await cancel_booking(db, user.get("id"))
                    if booking_result:
                        await message.answer("Your appointment has been cancelled.")
                    else:
                        await message.answer(
                            "Unexpected error, please contact your administrator"
                        )
                case _:
                    logging.info("Check your action in llm")

    else:
        await message.answer(llm_answer["output"])
