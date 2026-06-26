"""
User Model — Core Entity

Represents a user account in the system. Uses SQLAlchemy 2.0
mapped_column() style with full type annotations.

Inherits from:
    - UUIDMixin: provides UUID primary key (id)
    - TimestampMixin: provides created_at, updated_at
    - Base: SQLAlchemy declarative base
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    """
    User account model.

    Table: users
    Columns:
        id              UUID    (PK, from UUIDMixin)
        email           str     (unique, indexed, not null)
        hashed_password str     (bcrypt hash, not null)
        full_name       str     (optional)
        is_active       bool    (default True, for soft-delete)
        is_superuser    bool    (default False, for admin access)
        created_at      datetime (from TimestampMixin)
        updated_at      datetime (from TimestampMixin)
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User's email address (unique identifier for auth)",
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="bcrypt-hashed password (never store plain text!)",
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        comment="User's full display name",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
        comment="Whether the user account is active (soft-delete flag)",
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
        comment="Whether the user has admin privileges",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, active={self.is_active})>"
