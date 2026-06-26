"""
User Repository — Data Access Layer

Handles all database operations for the User model.
This is the ONLY place where SQL/ORM queries for users are written.

Rules:
    - No business logic (that belongs in services/)
    - Returns ORM models or None (never raises business exceptions)
    - All methods are async
    - Receives session via constructor injection
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.user import User

logger = get_logger(__name__)


class UserRepository:
    """
    Repository for User CRUD operations.

    All database queries for the User model are centralized here.
    Services call this repository — they never write raw SQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize with an async database session.

        The session is injected by FastAPI's dependency system,
        ensuring each request gets its own session.
        """
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a user by their UUID primary key."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by their email address."""
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> User:
        """
        Create a new user in the database.

        Args:
            user_data: dict with keys matching User model columns
                       (email, hashed_password, full_name, etc.)

        Returns:
            The created User instance with generated id and timestamps.
        """
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()  # Generate ID without committing
        await self.session.refresh(user)  # Load server-generated values
        logger.info("user_created", user_id=str(user.id), email=user.email)
        return user

    async def update(
        self, user_id: uuid.UUID, update_data: dict
    ) -> User | None:
        """
        Update a user's fields.

        Args:
            user_id: UUID of the user to update
            update_data: dict of fields to update (only non-None values)

        Returns:
            Updated User instance or None if user not found.
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)

        await self.session.flush()
        await self.session.refresh(user)
        logger.info("user_updated", user_id=str(user_id))
        return user

    async def deactivate(self, user_id: uuid.UUID) -> bool:
        """
        Soft-delete a user by setting is_active = False.

        We never hard-delete users — soft-delete preserves data
        for audit trails and potential account recovery.
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        user.is_active = False
        await self.session.flush()
        logger.info("user_deactivated", user_id=str(user_id))
        return True

    async def email_exists(self, email: str) -> bool:
        """Check if an email is already registered."""
        user = await self.get_by_email(email)
        return user is not None
