"""
Health Check Schemas — Response Models

Pydantic models for health check endpoint responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response for the basic liveness probe."""

    status: str = Field(
        ...,
        description="Health status",
        examples=["healthy"],
    )
    environment: str = Field(
        ...,
        description="Current environment",
        examples=["development"],
    )
    version: str = Field(
        ...,
        description="Application version",
        examples=["0.1.0"],
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp (UTC)",
    )


class ReadinessResponse(BaseModel):
    """Response for the readiness probe with component-level checks."""

    status: str = Field(
        ...,
        description="Overall readiness status",
        examples=["ready", "degraded"],
    )
    checks: dict[str, str] = Field(
        ...,
        description="Component-level health status",
        examples=[{"database": "connected", "redis": "connected"}],
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp (UTC)",
    )
