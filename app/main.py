import logging

from fastapi import FastAPI

from app.api.routes import health, leads, chat, faq
from app.config import get_settings
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa: F401

setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting AI Receptionist API...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables checked/created successfully.")


@app.get("/")
def root() -> dict:
    return {
        "message": "Welcome to AI Receptionist API",
        "environment": settings.app_env,
    }


app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(leads.router, prefix=settings.api_v1_prefix)
app.include_router(chat.router, prefix=settings.api_v1_prefix)
app.include_router(faq.router, prefix=settings.api_v1_prefix)