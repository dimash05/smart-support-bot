from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "/start - start the bot\n"
        "/help - show commands\n"
        "/faq - show faq\n"
        "/new_ticket - create a new ticket\n"
        "/my_tickets - show your tickets"
    )