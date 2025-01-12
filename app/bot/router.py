from aiogram import Router

from app.bot.handlers.faq import router as faq_router
from app.bot.handlers.help import router as help_router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.tickets import router as tickets_router

bot_router = Router()

bot_router.include_router(start_router)
bot_router.include_router(help_router)
bot_router.include_router(faq_router)
bot_router.include_router(tickets_router)