"""
Authentication Service — Business Logic

Orchestrates the authentication flow:
    - Register new users (validate, hash password, save)
    - Authenticate users (verify credentials, issue tokens)
    - Refresh access tokens
    - Get current user from token

Business rules enforced HERE (not in routes or repositories):
    - Email uniqueness
    - Password strength (delegated to schema validator)
    - Account activation status
    - Token type validation (access vs. refresh)
"""

import uuid

import jwt

from app.core.exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserCreate

logger = get_logger(__name__)


class AuthService:
    """
    Authentication business logic.

    This service orchestrates the auth flow by calling the repository
    for data access and the security module for cryptography.
    It contains ALL business rules — routes are thin wrappers.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """Inject the user repository (Dependency Inversion Principle)."""
        self.user_repo = user_repository

    async def register(self, user_data: UserCreate) -> User:
        """
        Register a new user account.

        Business rules:
            1. Email must not already exist
            2. Password is hashed before storage
            3. Email is normalized to lowercase

        Returns:
            Created User instance

        Raises:
            ConflictException: if email is already registered
        """
        # Check for existing email
        if await self.user_repo.email_exists(user_data.email):
            raise ConflictException(
                message=f"Email '{user_data.email}' is already registered"
            )

        # Hash the password (never store plain text!)
        hashed = hash_password(user_data.password)

        # Create the user
        user = await self.user_repo.create(
            {
                "email": user_data.email.lower(),
                "hashed_password": hashed,
                "full_name": user_data.full_name,
            }
        )

        logger.info("user_registered", user_id=str(user.id), email=user.email)
        return user

    async def authenticate(self, email: str, password: str) -> Token:
        """
        Authenticate a user and return JWT tokens.

        Business rules:
            1. User must exist
            2. Password must match
            3. Account must be active
            4. Return both access and refresh tokens

        Returns:
            Token with access_token, refresh_token, token_type

        Raises:
            UnauthorizedException: if credentials are invalid
        """
        # Find user by email
        user = await self.user_repo.get_by_email(email.lower())

        if user is None:
            # Don't reveal whether the email exists (security)
            raise UnauthorizedException(message="Invalid email or password")

        # Verify password
        if not verify_password(password, user.hashed_password):
            logger.warning(
                "login_failed_bad_password",
                email=email,
            )
            raise UnauthorizedException(message="Invalid email or password")

        # Check if account is active
        if not user.is_active:
            raise UnauthorizedException(message="Account is deactivated")

        # Generate tokens
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        logger.info("user_authenticated", user_id=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Exchange a refresh token for a new access token.

        Business rules:
            1. Refresh token must be valid and not expired
            2. Token type must be "refresh" (not "access")
            3. User must still exist and be active

        Returns:
            New Token with fresh access_token

        Raises:
            UnauthorizedException: if refresh token is invalid
        """
        try:
            payload = decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException(message="Refresh token has expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException(message="Invalid refresh token")

        # Verify it's a refresh token (not an access token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException(
                message="Invalid token type. Expected refresh token."
            )

        # Verify user still exists and is active
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException(message="Invalid token payload")

        user = await self.user_repo.get_by_id(uuid.UUID(user_id))
        if user is None or not user.is_active:
            raise UnauthorizedException(message="User not found or deactivated")

        # Issue new access token (keep the same refresh token)
        new_access_token = create_access_token(subject=str(user.id))

        logger.info("token_refreshed", user_id=str(user.id))

        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,  # Reuse existing refresh token
            token_type="bearer",
        )

    async def get_user_by_token(self, token: str) -> User:
        """
        Get the current user from an access token.

        Used by the get_current_user dependency.

        Raises:
            UnauthorizedException: if token is invalid or user not found
        """
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException(message="Access token has expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException(message="Invalid access token")

        if payload.get("type") != "access":
            raise UnauthorizedException(
                message="Invalid token type. Expected access token."
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException(message="Invalid token payload")

        user = await self.user_repo.get_by_id(uuid.UUID(user_id))
        if user is None:
            raise UnauthorizedException(message="User not found")
        if not user.is_active:
            raise UnauthorizedException(message="Account is deactivated")

        return user
