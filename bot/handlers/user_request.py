import logging

from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.voice)
async def voice_message_handler(message: Message):
    await message.reply_voice(message.voice.file_id)


@router.message(F.text)
async def text_message_handler(message: Message):
    await message.answer(message.text)
