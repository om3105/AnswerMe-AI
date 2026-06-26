"""
Core Layer — Application Infrastructure

Cross-cutting concerns required by the entire application:

    config.py     → Pydantic Settings (env vars, validation, defaults)
    security.py   → JWT token operations, password hashing
    logging.py    → Structured logging configuration (structlog)
    redis.py      → Async Redis connection management
    middleware.py → Request ID middleware for distributed tracing
    exceptions.py → Custom exception hierarchy and global handlers
"""
