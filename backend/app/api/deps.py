"""
Dependency Injection — Shared Dependencies

FastAPI dependency functions used across all endpoints.
Re-exports commonly used dependencies for convenient imports.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.redis import get_redis
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

# OAuth2 scheme — tells FastAPI to expect a Bearer token
# tokenUrl is the endpoint clients use to obtain tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Create a UserRepository with the current DB session."""
    return UserRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Create an AuthService with the UserRepository."""
    return AuthService(user_repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """
    Get the current authenticated user from the JWT token.

    This dependency:
        1. Extracts the Bearer token from the Authorization header
        2. Decodes and validates the JWT
        3. Fetches the user from the database
        4. Verifies the account is active

    Usage in endpoints:
        @router.get("/me")
        async def get_me(user: User = Depends(get_current_user)):
            return user

    Raises:
        UnauthorizedException: if token is missing, invalid, or user not found
    """
    return await auth_service.get_user_by_token(token)


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current user and verify they are a superuser.

    Used for admin-only endpoints.
    """
    from app.core.exceptions import ForbiddenException

    if not current_user.is_superuser:
        raise ForbiddenException(message="Superuser access required")
    return current_user


# Re-export for convenient imports
__all__ = [
    "get_db",
    "get_redis",
    "get_settings",
    "get_current_user",
    "get_current_active_superuser",
    "get_auth_service",
    "get_user_repository",
    "oauth2_scheme",
    "Settings",
]
