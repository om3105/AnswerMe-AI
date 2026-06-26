"""
User Schemas — Request/Response Models

Pydantic models for user-related API operations.
Each schema has a specific purpose — never reuse a single schema
for both input and output (security risk: exposing hashed_password).
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """Request body for POST /auth/register."""

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (min 8 characters)",
        examples=["StrongP@ss123"],
    )
    full_name: str | None = Field(
        None,
        max_length=255,
        description="User's full name",
        examples=["Om Deo"],
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Enforce basic password strength requirements.

        Production apps should use more comprehensive checks
        (e.g., zxcvbn library for password strength estimation).
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    """Request body for POST /auth/login."""

    email: EmailStr = Field(
        ...,
        description="Registered email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        description="Account password",
        examples=["StrongP@ss123"],
    )


class UserResponse(BaseModel):
    """
    Response body for user data.

    NEVER includes hashed_password or other sensitive fields.
    This is what clients see — always safe to return.
    """

    id: uuid.UUID = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    full_name: str | None = Field(None, description="User's full name")
    is_active: bool = Field(..., description="Whether the account is active")
    is_superuser: bool = Field(..., description="Whether the user is an admin")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Request body for PATCH /users/{id}. All fields optional."""

    full_name: str | None = Field(None, max_length=255)
    password: str | None = Field(None, min_length=8, max_length=128)
