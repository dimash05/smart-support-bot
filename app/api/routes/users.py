from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session_dependency
from app.schemas.user import UserRead
from app.services.admin_user_service import AdminUserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
async def list_users(
    session: AsyncSession = Depends(db_session_dependency),
) -> list[UserRead]:
    service = AdminUserService(session)
    return await service.get_all_users()