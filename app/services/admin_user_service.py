from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AdminUserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> list[User]:
        stmt = select(User).order_by(User.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())