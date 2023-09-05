from aiogram import F, Router
from aiogram.types import Message
from langchain.agents import initialize_agent, AgentType
import logging
from models.conversation_chain import tools, llm
from common.cache import user_agent_dict

router = Router()


@router.message(F.voice)
async def voice_message_handler(message: Message):
    await message.reply_voice(message.voice.file_id)


@router.message(F.text)
async def text_message_handler(message: Message):
    if not user_agent_dict.get(message.from_user.id, None):
        user_agent_dict[message.from_user.id] = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
    try:
        answer = user_agent_dict[message.from_user.id].run(message.text)
        await message.answer(f"bot query: {message.text}, answer: {answer}")
    except Exception as err:
        logging.error(err)
        await message.answer(f"bot query: {message.text}, error: {err}")
