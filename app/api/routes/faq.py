from fastapi import APIRouter

router = APIRouter(prefix="/faq", tags=["FAQ"])


@router.get("")
async def list_faq_entries() -> dict:
    return {"items": [], "message": "FAQ endpoint placeholder"}