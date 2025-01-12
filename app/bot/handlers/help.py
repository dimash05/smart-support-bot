from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Available commands:\n\n"
        "/start - register and open main menu\n"
        "/help - show this message\n"
        "/faq - browse common questions\n"
        "/new_ticket - create a support ticket\n"
        "/my_tickets - show your tickets"
    )