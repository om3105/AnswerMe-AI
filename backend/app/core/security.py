"""
Security — JWT Tokens & Password Hashing

Handles all authentication cryptography:
    - Password hashing with bcrypt (via passlib)
    - JWT token creation and validation
    - Access token + refresh token pattern

Implementation will be completed in Step 5 (Authentication).
This module provides the security utility functions.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

# ── Password Hashing ────────────────────────────────────────
# bcrypt is intentionally slow (adaptive cost factor).
# This makes brute-force attacks computationally expensive.
# schemes=["bcrypt"]: use bcrypt as the hashing algorithm
# deprecated="auto": automatically upgrade old hashes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Token Operations ────────────────────────────────────

def create_access_token(
    subject: str,
    extra_data: dict[str, Any] | None = None,
) -> str:
    """
    Create a short-lived access token.

    Args:
        subject: The token subject (typically user ID as string)
        extra_data: Additional claims to include in the payload

    Returns:
        Encoded JWT string
    """
    settings = get_settings()
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + expires_delta,
        "iat": datetime.now(UTC),
        "type": "access",
    }
    if extra_data:
        payload.update(extra_data)

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(
    subject: str,
    extra_data: dict[str, Any] | None = None,
) -> str:
    """
    Create a long-lived refresh token.

    Refresh tokens are used ONLY to obtain new access tokens.
    They should be stored securely (httpOnly cookie or secure storage).
    """
    settings = get_settings()
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + expires_delta,
        "iat": datetime.now(UTC),
        "type": "refresh",
    }
    if extra_data:
        payload.update(extra_data)

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Raises:
        jwt.ExpiredSignatureError: Token has expired
        jwt.InvalidTokenError: Token is invalid (tampered, malformed)
    """
    settings = get_settings()

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
