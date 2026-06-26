"""
Async Database Session Factory

Creates and manages the async SQLAlchemy engine and session.
Uses asyncpg as the PostgreSQL driver for non-blocking I/O.

Key concepts:
    - Engine: manages the connection pool (one per application)
    - Session: a unit of work (one per request, auto-committed or rolled back)
    - Connection pool: reuses connections instead of creating new ones per query
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# ── Engine Configuration ─────────────────────────────────────
# The engine is created once and shared across the entire application.
# It manages the connection pool internally.

settings = get_settings()

async_engine = create_async_engine(
    settings.DATABASE_URL,
    # Connection pool settings
    pool_size=settings.DB_POOL_SIZE,        # Persistent connections
    max_overflow=settings.DB_MAX_OVERFLOW,   # Extra connections under load
    pool_timeout=settings.DB_POOL_TIMEOUT,   # Wait time for a connection
    pool_recycle=settings.DB_POOL_RECYCLE,   # Recycle stale connections
    pool_pre_ping=True,                      # Test connections before use
    # Echo SQL queries in debug mode (useful for development)
    echo=settings.DEBUG and settings.ENVIRONMENT == "development",
)

# ── Session Factory ──────────────────────────────────────────
# async_sessionmaker creates a factory that produces AsyncSession instances.
# expire_on_commit=False: don't expire objects after commit
#   (avoids lazy-loading issues in async context)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that yields a database session for each request.

    Usage in FastAPI:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...

    The session is automatically committed on success or rolled back
    on exception, then closed when the request completes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize the database connection on application startup.

    Tests the connection and logs the result.
    Tables are created by Alembic migrations, not here.
    """
    try:
        async with async_engine.begin() as conn:
            # Simple query to verify connectivity
            await conn.execute(
                # text() is imported in the calling module
                __import__("sqlalchemy").text("SELECT 1")
            )
        logger.info("database_connected", url=settings.DATABASE_URL.split("@")[-1])
    except Exception as e:
        logger.error("database_connection_failed", error=str(e))
        raise


async def close_db() -> None:
    """Dispose of the engine's connection pool on application shutdown."""
    await async_engine.dispose()
    logger.info("database_disconnected")
