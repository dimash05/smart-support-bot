from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session_dependency
from app.schemas.faq import FAQCreate, FAQRead, FAQUpdate
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faq", tags=["FAQ"])


@router.get("", response_model=list[FAQRead])
async def list_faq_entries(
    session: AsyncSession = Depends(db_session_dependency),
) -> list[FAQRead]:
    service = FAQService(session)
    return await service.get_all_entries()


@router.post("", response_model=FAQRead, status_code=status.HTTP_201_CREATED)
async def create_faq_entry(
    payload: FAQCreate,
    session: AsyncSession = Depends(db_session_dependency),
) -> FAQRead:
    service = FAQService(session)
    return await service.create_entry(payload)


@router.patch("/{faq_id}", response_model=FAQRead)
async def update_faq_entry(
    payload: FAQUpdate,
    faq_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(db_session_dependency),
) -> FAQRead:
    service = FAQService(session)
    entry = await service.update_entry(faq_id, payload)

    if entry is None:
        raise HTTPException(status_code=404, detail="FAQ entry not found")

    return entry