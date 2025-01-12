import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards.reply import get_main_keyboard
from app.db.session import SessionLocal
from app.services.user_service import UserService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("Could not read Telegram user data.")
        return

    async with SessionLocal() as session:
        service = UserService(session)

        try:
            await service.get_or_create_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )
        except Exception:
            logger.exception("Failed to register Telegram user")
            await message.answer("Something went wrong while saving your profile.")
            return

    await message.answer(
        "Welcome to Smart Support Bot.\n"
        "You can browse FAQ, create tickets and track your requests.",
        reply_markup=get_main_keyboard(),
    )