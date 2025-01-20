from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session_dependency
from app.schemas.ticket import TicketRead, TicketStatusUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("", response_model=list[TicketRead])
async def list_tickets(
    session: AsyncSession = Depends(db_session_dependency),
) -> list[TicketRead]:
    service = TicketService(session)
    return await service.get_all_tickets()


@router.patch("/{ticket_id}/status", response_model=TicketRead)
async def update_ticket_status(
    payload: TicketStatusUpdate,
    ticket_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(db_session_dependency),
) -> TicketRead:
    service = TicketService(session)
    ticket = await service.update_ticket_status(ticket_id, payload.status)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket