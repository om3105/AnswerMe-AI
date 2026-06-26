"""
Core Layer — Application Infrastructure

This package contains cross-cutting concerns that don't belong to
any specific feature but are required by the entire application:

    config.py   → Pydantic Settings (env vars, validation, defaults)
    security.py → JWT token operations, password hashing
    logging.py  → Structured logging configuration (structlog)

Why "core" is separate from "services":
    - Core = infrastructure (HOW things work)
    - Services = business logic (WHAT the app does)
    - This separation follows the Dependency Rule in Clean Architecture:
      inner layers (services) depend on abstractions, not on outer layers (core)
"""
