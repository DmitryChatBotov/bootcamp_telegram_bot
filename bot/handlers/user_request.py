import io
import json
import logging
from os import getenv

from aiogram import Bot, F, Router
from aiogram.types import Message
from crud.booking import booking, cancel_booking
from crud.conversation import chat_with_llm
from crud.user import get_user
from db import Database
from models import whisper_model

router = Router()


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
    logging.info(llm_answer)
    agent_result = llm_answer.get("intermediate_steps")[-1][-1]
    logging.info(agent_result)
    if isinstance(agent_result, dict):
        async with Database(getenv("SQLITE_FILE")) as db:
            user = await get_user(db, message.from_user.id)
            match agent_result.get("action"):
                case "Create":
                    # отправляем сообщение в CRM
                    booking_result = await booking(
                        db=db,
                        master_name=agent_result.get("master_name", None),
                        service_name=agent_result.get("beauty_service"),
                        client_name=user.get("name"),
                        booking_time=agent_result.get("booking_time"),
                        booking_date=agent_result.get("booking_date"),
                    )
                    if booking_result:
                        template = f"You have been enrolled to the master {booking_result.get('master_name')}. Date: {booking_result.get('date')}. Time: {booking_result.get('time')}. Service: {booking_result.get('service_name')}. Price: {booking_result.get('price')}"
                        await message.answer(template)
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
