from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.faq import FAQEntry
from app.schemas.faq import FAQCreate, FAQUpdate


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

    async def get_all_entries(self) -> list[FAQEntry]:
        stmt = select(FAQEntry).order_by(FAQEntry.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, faq_id: int) -> FAQEntry | None:
        stmt = select(FAQEntry).where(FAQEntry.id == faq_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_entry(self, data: FAQCreate) -> FAQEntry:
        entry = FAQEntry(
            question=data.question,
            answer=data.answer,
            is_published=data.is_published,
        )
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def update_entry(self, faq_id: int, data: FAQUpdate) -> FAQEntry | None:
        entry = await self.get_by_id(faq_id)
        if entry is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field_name, value in update_data.items():
            setattr(entry, field_name, value)

        await self.session.commit()
        await self.session.refresh(entry)
        return entry