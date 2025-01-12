import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.session import SessionLocal
from app.services.faq_service import FAQService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("faq"))
async def faq_handler(message: Message) -> None:
    async with SessionLocal() as session:
        service = FAQService(session)

        try:
            faq_entries = await service.get_published_entries()
        except Exception:
            logger.exception("Failed to fetch FAQ entries")
            await message.answer("Could not load FAQ right now.")
            return

    if not faq_entries:
        await message.answer("FAQ is empty right now.")
        return

    parts: list[str] = []
    for index, entry in enumerate(faq_entries, start=1):
        parts.append(f"{index}. {entry.question}\n{entry.answer}")

    await message.answer("\n\n".join(parts))