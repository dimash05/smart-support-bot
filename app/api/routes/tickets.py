from fastapi import APIRouter

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("")
async def list_tickets() -> dict:
    return {"items": [], "message": "Tickets endpoint placeholder"}