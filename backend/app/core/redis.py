"""
Redis Connection Manager

Provides async Redis client for caching, rate limiting, and session storage.
Uses redis.asyncio for non-blocking operations.
"""

import redis.asyncio as aioredis

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Global Redis client (initialized on app startup)
redis_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    """
    Initialize the Redis connection on application startup.

    Returns the Redis client for use in dependency injection.
    """
    global redis_client

    settings = get_settings()

    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        # Connection pool settings
        max_connections=20,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
    )

    # Test connection
    try:
        await redis_client.ping()
        logger.info("redis_connected", url=settings.REDIS_URL)
    except Exception as e:
        logger.error("redis_connection_failed", error=str(e))
        raise

    return redis_client


async def close_redis() -> None:
    """Close the Redis connection on application shutdown."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        logger.info("redis_disconnected")


def get_redis() -> aioredis.Redis:
    """
    Get the Redis client for dependency injection.

    Usage:
        @router.get("/cached-data")
        async def get_data(redis: Redis = Depends(get_redis)):
            cached = await redis.get("key")
    """
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    return redis_client
