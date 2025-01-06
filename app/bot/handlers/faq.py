from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("faq"))
async def faq_handler(message: Message) -> None:
    await message.answer("FAQ is empty right now.")