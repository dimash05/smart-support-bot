from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.models.user import User
from app.utils.enums import TicketStatus


class TicketService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_ticket(
        self,
        user: User,
        category: str,
        title: str,
        description: str,
    ) -> Ticket:
        ticket = Ticket(
            user_id=user.id,
            category=category,
            title=title,
            description=description,
            status=TicketStatus.OPEN.value,
        )
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def get_user_tickets(self, user_id: int) -> list[Ticket]:
        stmt = (
            select(Ticket)
            .where(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_tickets(self) -> list[Ticket]:
        stmt = select(Ticket).order_by(Ticket.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_ticket_by_id(self, ticket_id: int) -> Ticket | None:
        stmt = select(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_ticket_status(
        self,
        ticket_id: int,
        status: TicketStatus,
    ) -> Ticket | None:
        ticket = await self.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None

        ticket.status = status.value
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket