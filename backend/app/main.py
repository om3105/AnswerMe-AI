"""
AnswerMe AI — FastAPI Application Entry Point

This module creates and configures the FastAPI application instance.

Responsibilities:
    1. Create the FastAPI app with metadata (title, version, docs URL)
    2. Register lifespan events (startup → connect DB/Redis, shutdown → disconnect)
    3. Include API routers (v1)
    4. Add middleware (CORS, Request ID)
    5. Register global exception handlers

Usage:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import v1_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.core.middleware import RequestIDMiddleware
from app.core.redis import close_redis, init_redis
from app.db.session import close_db, init_db


# ── Lifespan Events ─────────────────────────────────────────
# FastAPI's lifespan context manager replaces the deprecated
# @app.on_event("startup") and @app.on_event("shutdown") decorators.
#
# Everything before `yield` runs on startup.
# Everything after `yield` runs on shutdown.

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan: startup and shutdown events.

    Startup:
        1. Configure structured logging
        2. Connect to PostgreSQL
        3. Connect to Redis
        4. Log startup complete

    Shutdown:
        1. Close Redis connection
        2. Close database connection pool
        3. Log shutdown complete
    """
    # ── Startup ──────────────────────────────────────────
    setup_logging()
    logger = get_logger(__name__)

    settings = get_settings()
    logger.info(
        "app_starting",
        app_name=settings.APP_NAME,
        environment=settings.ENVIRONMENT,
        debug=settings.DEBUG,
    )

    # Connect to database
    await init_db()

    # Connect to Redis
    await init_redis()

    logger.info("app_started", app_name=settings.APP_NAME)

    yield  # ← Application runs here

    # ── Shutdown ─────────────────────────────────────────
    logger.info("app_shutting_down")

    await close_redis()
    await close_db()

    logger.info("app_shutdown_complete")


# ── Create FastAPI Application ───────────────────────────────

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the FastAPI application.

    Using a factory function (instead of a module-level `app = FastAPI()`)
    allows us to:
        - Create multiple app instances for testing
        - Pass different configurations
        - Keep imports clean
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Enterprise-Grade AI Knowledge Assistant API. "
            "Built with FastAPI, PostgreSQL, Redis, and Clean Architecture."
        ),
        version="0.1.0",
        # API documentation URLs
        docs_url="/docs",       # Swagger UI
        redoc_url="/redoc",     # ReDoc
        openapi_url="/openapi.json",
        # Lifespan manager for startup/shutdown
        lifespan=lifespan,
        # Disable docs in production (optional, commented out for now)
        # docs_url=None if settings.is_production else "/docs",
    )

    # ── Middleware ────────────────────────────────────────
    # Middleware is executed in REVERSE order of registration.
    # Last registered = first to execute.

    # 1. CORS — must be first (outermost) to handle preflight requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # 2. Request ID — generates unique ID per request for tracing
    app.add_middleware(RequestIDMiddleware)

    # ── Exception Handlers ───────────────────────────────
    register_exception_handlers(app)

    # ── Routers ──────────────────────────────────────────
    app.include_router(v1_router)

    return app


# ── Module-level app instance ────────────────────────────────
# This is what uvicorn imports: `uvicorn app.main:app`
app = create_app()
