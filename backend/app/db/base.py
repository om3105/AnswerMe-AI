"""
SQLAlchemy Declarative Base

All ORM models inherit from this Base class.
This provides:
    - Table name auto-generation
    - Common columns (id, created_at, updated_at) via mixins
    - Metadata for Alembic migrations

Usage:
    from app.db.base import Base

    class User(Base):
        __tablename__ = "users"
        ...
"""
