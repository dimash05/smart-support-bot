import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.router import bot_router
from app.config.logging import setup_logging
from app.config.settings import get_settings


async def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(bot_router)

    logging.getLogger(__name__).info("Starting bot polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())