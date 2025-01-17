"""
Starting point for the execution of the API server.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins import RequestIdPlugin
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
import dotenv
import os

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.logging_config import setup_logging

tags_metadata = [
    {
        "name": "login",
        "description": "Endpoints for obtaining access tokens and password recovery.",
    },
    {
        "name": "utils",
        "description": (
            "Endpoint for sending test emails. " "**Needs superuser privileges.**"
        ),
    },
    {
        "name": "users",
        "description": (
            "Endpoint for handling CRUD operations on users, fetching questions "
            "corresponding to the users, verifying their answers, and obtaining the "
            "leaderboard."
        ),
    },
    {
        "name": "questions",
        "description": (
            "Endpoint for handling CRUD operations on questions. "
            "**Needs superuser privileges.**"
        ),
    },
    {
        "name": "questions_order",
        "description": (
            "Endpoint for associating questions with question numbers. "
            "**Needs superuser privileges.**"
        ),
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    contact={
        "name": "Sanchith Hegde",
        "url": "https://github.com/SanchithHegde",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/SanchithHegde/decrypto-api/blob/main/LICENSE",
    },
)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Defines tasks performed on application startup.
    """

    setup_logging()


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(RawContextMiddleware, plugins=[RequestIdPlugin()])

limiter = Limiter(
    key_func=get_remote_address,
    application_limits=[os.environ.get("RATE_LIMIT", "30/minute")],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
