from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.faq import FAQEntry


class FAQService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_published_entries(self) -> list[FAQEntry]:
        stmt = (
            select(FAQEntry)
            .where(FAQEntry.is_published.is_(True))
            .order_by(FAQEntry.id.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())