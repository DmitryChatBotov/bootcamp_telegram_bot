import io
import logging
from os import getenv

from aiogram import Bot, F, Router
from aiogram.types import Message, Voice
from pydub import AudioSegment

from common.cache import user_agent_dict
from models import whisper_model
from models.langchain import ConversationAgent, llm

router = Router()


@router.message(F.voice)
async def voice_message_handler(message: Message, bot: Bot):
    voice_file_info = await bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)
    voice_mp3_path = f"voice-{message.voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(voice_mp3_path, format="mp3")
    result = whisper_model(voice_mp3_path)
    await message.answer(result)


@router.message(F.text)
async def text_message_handler(message: Message):
    if not user_agent_dict.get(message.from_user.id, None):
        user_agent_dict[message.from_user.id] = ConversationAgent(
            llm, getenv("SQLITE_FILE")
        )
    try:
        answer = user_agent_dict[message.from_user.id](message.text)
        await message.answer(f"bot query: {message.text}, answer: {answer}")
    except Exception as err:
        logging.error(err)
        await message.answer(f"bot query: {message.text}, error: {err}")
