from fastapi import FastAPI

from app.api.router import api_router
from app.config.logging import setup_logging
from app.config.settings import get_settings

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(
    title="smart-support-bot API",
    version="0.1.0",
)

app.include_router(api_router, prefix=settings.api_prefix)