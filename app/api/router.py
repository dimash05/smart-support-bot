from fastapi import APIRouter

from app.api.routes.faq import router as faq_router
from app.api.routes.tickets import router as tickets_router
from app.api.routes.users import router as users_router

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
async def healthcheck() -> dict:
    return {"status": "ok"}


api_router.include_router(users_router)
api_router.include_router(tickets_router)
api_router.include_router(faq_router)