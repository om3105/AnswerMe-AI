"""
Token Schemas — JWT Request/Response Models

Pydantic models for JWT token operations.
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Response body containing JWT tokens."""

    access_token: str = Field(
        ...,
        description="Short-lived access token for API calls",
    )
    refresh_token: str = Field(
        ...,
        description="Long-lived token for obtaining new access tokens",
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')",
    )


class TokenPayload(BaseModel):
    """Decoded JWT payload contents."""

    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued-at timestamp")
    type: str = Field(..., description="Token type ('access' or 'refresh')")


class RefreshTokenRequest(BaseModel):
    """Request body for POST /auth/refresh."""

    refresh_token: str = Field(
        ...,
        description="The refresh token to exchange for a new access token",
    )
