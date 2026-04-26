import logging

from fastapi import FastAPI

from app.api.routes import health, leads, chat, faq, bookings, followups, admin, dashboard, calendar, messaging
from app.config import get_settings
from app.core.logging import setup_logging

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
app.include_router(bookings.router, prefix=settings.api_v1_prefix)
app.include_router(followups.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
app.include_router(calendar.router, prefix=settings.api_v1_prefix)
app.include_router(messaging.router, prefix=settings.api_v1_prefix)