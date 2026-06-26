"""
Configuration Management — Pydantic Settings

This module uses pydantic-settings to:
    1. Load environment variables from .env files
    2. Validate types and constraints at startup
    3. Provide type-safe access to all config values
    4. Support environment-specific overrides (dev/staging/prod)

Why Pydantic Settings?
    - Fails fast: invalid config crashes at startup, not at 3 AM in production
    - Type safety: DATABASE_URL is a string, PORT is an int — enforced
    - Defaults: sensible defaults for development, overridden in production
    - Single source of truth: one Settings class, used everywhere via DI

Pattern:
    settings = Settings()  # Loads from env vars + .env file
    # Access: settings.DATABASE_URL, settings.JWT_SECRET_KEY, etc.
"""
