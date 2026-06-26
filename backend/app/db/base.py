"""
SQLAlchemy Declarative Base

All ORM models inherit from this Base class.
Provides common columns (id, created_at, updated_at) via a mixin
so every table automatically gets consistent metadata fields.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    All models that inherit from this class will automatically
    be discovered by Alembic for migration generation.

    Usage:
        class User(Base):
            __tablename__ = "users"
            # ... your columns
    """

    pass


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at columns to any model.

    Usage:
        class User(TimestampMixin, Base):
            __tablename__ = "users"

    Why a mixin?
        - DRY: every table needs timestamps, define once
        - Consistency: all tables use the same column names and types
        - Server-side defaults: the database generates timestamps,
          not Python (handles timezone issues correctly)
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDMixin:
    """
    Mixin that adds a UUID primary key column.

    Why UUIDs over auto-increment integers?
        - No sequential guessing (security: can't enumerate /users/1, /users/2)
        - Safe for distributed systems (no central ID authority)
        - Can be generated client-side before INSERT
        - Harder to accidentally leak record count
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
