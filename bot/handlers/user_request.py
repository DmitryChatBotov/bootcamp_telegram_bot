import io
import logging
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.types import Message

from crud.conversation import chat_with_llm
from models import whisper_model

router = Router()


@router.message(F.voice)
async def voice_message_handler(message: Message, bot: Bot):
    voice_file_info = await bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    start = datetime.now()
    result = whisper_model(voice_ogg)
    logging.info(
        f"result {result}, duration: {(datetime.now() - start).total_seconds()}"
    )
    answer = chat_with_llm(message.from_user.id, message.text)
    await message.answer(answer)


@router.message(F.text)
async def text_message_handler(message: Message):
    answer = chat_with_llm(message.from_user.id, message.text)
    await message.answer(answer)
