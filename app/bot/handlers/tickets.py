import logging
from datetime import timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.states.ticket import CreateTicketStates
from app.db.session import SessionLocal
from app.services.ticket_service import TicketService
from app.services.user_service import UserService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("new_ticket"))
async def new_ticket_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(CreateTicketStates.waiting_for_category)
    await message.answer(
        "Let's create a new ticket.\n\n"
        "Send ticket category.\n"
        "For example: Billing, Technical issue, Account, Other."
    )


@router.message(CreateTicketStates.waiting_for_category)
async def ticket_category_handler(message: Message, state: FSMContext) -> None:
    category = (message.text or "").strip()

    if len(category) < 2 or len(category) > 100:
        await message.answer("Category should be between 2 and 100 characters.")
        return

    await state.update_data(category=category)
    await state.set_state(CreateTicketStates.waiting_for_title)
    await message.answer("Now send a short ticket title.")


@router.message(CreateTicketStates.waiting_for_title)
async def ticket_title_handler(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()

    if len(title) < 3 or len(title) > 255:
        await message.answer("Title should be between 3 and 255 characters.")
        return

    await state.update_data(title=title)
    await state.set_state(CreateTicketStates.waiting_for_description)
    await message.answer("Now describe the issue in more detail.")


@router.message(CreateTicketStates.waiting_for_description)
async def ticket_description_handler(message: Message, state: FSMContext) -> None:
    description = (message.text or "").strip()

    if len(description) < 10 or len(description) > 5000:
        await message.answer("Description should be between 10 and 5000 characters.")
        return

    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("Could not read Telegram user data.")
        await state.clear()
        return

    data = await state.get_data()

    async with SessionLocal() as session:
        user_service = UserService(session)
        ticket_service = TicketService(session)

        try:
            user = await user_service.get_or_create_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )

            ticket = await ticket_service.create_ticket(
                user=user,
                category=data["category"],
                title=data["title"],
                description=description,
            )
        except Exception:
            logger.exception("Failed to create ticket")
            await message.answer("Something went wrong while creating the ticket.")
            await state.clear()
            return

    await state.clear()
    await message.answer(
        f"Ticket created successfully.\n\n"
        f"ID: {ticket.id}\n"
        f"Category: {ticket.category}\n"
        f"Title: {ticket.title}\n"
        f"Status: {ticket.status}"
    )


@router.message(Command("my_tickets"))
async def my_tickets_handler(message: Message) -> None:
    telegram_user = message.from_user
    if telegram_user is None:
        await message.answer("Could not read Telegram user data.")
        return

    async with SessionLocal() as session:
        user_service = UserService(session)
        ticket_service = TicketService(session)

        try:
            user = await user_service.get_by_telegram_id(telegram_user.id)
            if user is None:
                await message.answer("No profile found. Use /start first.")
                return

            tickets = await ticket_service.get_user_tickets(user.id)
        except Exception:
            logger.exception("Failed to fetch user tickets")
            await message.answer("Could not load your tickets right now.")
            return

    if not tickets:
        await message.answer("You do not have any tickets yet.")
        return

    parts: list[str] = []
    for ticket in tickets:
        created_at = ticket.created_at
        if created_at.tzinfo is not None:
            created_at = created_at.astimezone(timezone.utc)

        parts.append(
            f"#{ticket.id} | {ticket.status}\n"
            f"Category: {ticket.category}\n"
            f"Title: {ticket.title}\n"
            f"Created: {created_at.strftime('%Y-%m-%d %H:%M')}"
        )

    await message.answer("\n\n".join(parts))


@router.message(F.text == "/cancel")
async def cancel_ticket_creation(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no active action to cancel.")
        return

    await state.clear()
    await message.answer("Ticket creation cancelled.")