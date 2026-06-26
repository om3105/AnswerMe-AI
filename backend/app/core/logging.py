"""
Structured Logging — structlog Configuration

Configures application-wide logging with two output modes:
    - Development: Colored, human-readable console output
    - Production: JSON-formatted output for log aggregation (ELK, Datadog)

Every log entry automatically includes:
    - timestamp (ISO 8601)
    - log level
    - event name
    - request_id (if in request context)
    - any additional key-value pairs
"""

import logging
import sys
from typing import Any

import structlog

from app.core.config import get_settings


def setup_logging() -> None:
    """
    Configure structlog and stdlib logging for the entire application.

    This function should be called ONCE during application startup.
    """
    settings = get_settings()

    # Determine log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Shared processors used in both dev and prod
    shared_processors: list[Any] = [
        # Add log level to the event dict
        structlog.stdlib.add_log_level,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Add timestamp in ISO 8601 format
        structlog.processors.TimeStamper(fmt="iso"),
        # If the event dict contains a stack trace, format it
        structlog.processors.StackInfoRenderer(),
        # Format exceptions
        structlog.processors.format_exc_info,
        # Decode bytes to strings
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.is_development:
        # Development: pretty, colored console output
        renderer = structlog.dev.ConsoleRenderer(
            colors=True,
            pad_event=40,
        )
    else:
        # Production: JSON output for log aggregation
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            # Filter by log level
            structlog.stdlib.filter_by_level,
            *shared_processors,
            # Prepare for stdlib integration
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        # Use stdlib's logging as the backend
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Cache logger instances for performance
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging to use structlog's formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            # Extract from the event dict
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            *shared_processors,
            renderer,
        ],
    )

    # Set up the root handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Suppress noisy third-party loggers
    for logger_name in ["uvicorn.access", "sqlalchemy.engine"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    # Allow SQLAlchemy engine logs in debug mode
    if settings.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Get a structlog logger instance.

    Usage:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("user_registered", user_id=42, email="user@example.com")
    """
    return structlog.get_logger(name)
