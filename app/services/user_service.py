import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create_user(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name

            try:
                await self.session.commit()
                await self.session.refresh(user)
            except Exception:
                await self.session.rollback()
                logger.exception("Failed to update existing user")
                raise

            return user

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        self.session.add(user)

        try:
            await self.session.commit()
            await self.session.refresh(user)
        except Exception:
            await self.session.rollback()
            logger.exception("Failed to create user")
            raise

        return user