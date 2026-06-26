"""
Dependency Injection — Shared Dependencies

FastAPI dependency functions used across all endpoints.
Dependencies are injected via FastAPI's Depends() mechanism.

This module re-exports commonly used dependencies so route handlers
can import from a single location:
    from app.api.deps import get_db, get_redis, get_settings
"""

from app.core.config import Settings, get_settings
from app.core.redis import get_redis
from app.db.session import get_db

# Re-export for convenient imports in endpoints
__all__ = [
    "get_db",
    "get_redis",
    "get_settings",
    "Settings",
]
