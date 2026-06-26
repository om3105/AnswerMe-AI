"""
Dependency Injection — Shared Dependencies

This module provides FastAPI dependency functions used across endpoints.
Dependencies are injected via FastAPI's `Depends()` mechanism.

Responsibilities:
    - get_db()           → Yields an async database session
    - get_redis()        → Returns the Redis client
    - get_current_user() → Validates JWT and returns the authenticated user
    - get_settings()     → Returns the application settings singleton

Why dependency injection?
    - Decouples route handlers from infrastructure (DB, cache, auth)
    - Makes testing trivial (swap real DB for mock)
    - Single source of truth for shared resources
    - Follows the Dependency Inversion Principle (SOLID "D")
"""
