from os import getenv

from aiogram import F, Router
from aiogram.types import Message
import logging
from models import ConversationAgent, llm
from common.cache import user_agent_dict

router = Router()


@router.message(F.voice)
async def voice_message_handler(message: Message):
    await message.reply_voice(message.voice.file_id)


@router.message(F.text)
async def text_message_handler(message: Message):
    if not user_agent_dict.get(message.from_user.id, None):
        user_agent_dict[message.from_user.id] = ConversationAgent(llm, getenv('SQLITE_FILE'))
    try:
        answer = user_agent_dict[message.from_user.id](message.text)
        await message.answer(f"bot query: {message.text}, answer: {answer}")
    except Exception as err:
        logging.error(err)
        await message.answer(f"bot query: {message.text}, error: {err}")
