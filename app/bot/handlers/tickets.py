from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("new_ticket"))
async def new_ticket_handler(message: Message) -> None:
    await message.answer("Ticket creation flow will be added in the next step.")


@router.message(Command("my_tickets"))
async def my_tickets_handler(message: Message) -> None:
    await message.answer("Your tickets list will appear here later.")