from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def list_users() -> dict:
    return {"items": [], "message": "Users endpoint placeholder"}