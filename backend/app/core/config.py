"""
Configuration Management — Pydantic Settings

Loads and validates all environment variables at application startup.
If any required variable is missing or has an invalid type, the app
crashes immediately with a clear error message — not at 3 AM in production.

Uses pydantic-settings v2 which reads from:
    1. Environment variables (highest priority)
    2. .env file (fallback for local development)
    3. Default values (lowest priority)
"""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All fields are typed and validated. Missing required fields
    or type mismatches will raise a ValidationError at startup.
    """

    # ── Application ──────────────────────────────────────────
    APP_NAME: str = "AnswerMe AI"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    # ── Backend Server ───────────────────────────────────────
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_WORKERS: int = 1

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://answerme:change_me_in_production@postgres:5432/answerme_db"

    # Connection pool settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # Recycle connections after 30 minutes

    # ── Redis ────────────────────────────────────────────────
    REDIS_URL: str = "redis://redis:6379/0"

    # ── JWT Authentication ───────────────────────────────────
    JWT_SECRET_KEY: str = "change-this-to-a-long-random-string-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ─────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost"]

    # ── Computed Properties ──────────────────────────────────
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    # ── Validators ───────────────────────────────────────────
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """
        Parse CORS origins from environment variable.
        Accepts both JSON string and Python list.
        """
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, treat as comma-separated
                return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is a valid Python logging level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(
                f"Invalid LOG_LEVEL '{v}'. Must be one of: {valid_levels}"
            )
        return upper_v

    # ── Pydantic Settings Configuration ──────────────────────
    model_config = SettingsConfigDict(
        # Read from .env file in the backend directory
        env_file=".env",
        # .env file is optional (env vars take priority)
        env_file_encoding="utf-8",
        # Case-insensitive env var names
        case_sensitive=False,
        # Extra fields are ignored (don't crash on unknown env vars)
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Create and cache a Settings instance.

    Using @lru_cache ensures we only parse environment variables once.
    The same Settings object is reused for all subsequent calls.
    This is a singleton pattern implemented via caching.
    """
    return Settings()
