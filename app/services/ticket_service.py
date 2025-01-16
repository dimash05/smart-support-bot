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