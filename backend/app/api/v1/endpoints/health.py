"""
Health Check Endpoints

Provides liveness and readiness probes for container orchestration.

Routes:
    GET /health          → Basic liveness (is the process alive?)
    GET /health/ready    → Readiness (can it handle traffic? checks DB + Redis)
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.health import HealthResponse, ReadinessResponse

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Basic health check. Returns 200 if the process is alive.",
)
async def health_check() -> HealthResponse:
    """
    Liveness probe — is the process alive?

    Used by Docker HEALTHCHECK and Kubernetes liveness probes.
    This should NEVER depend on external services (DB, Redis).
    If this fails, the container should be restarted.
    """
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version="0.1.0",
        timestamp=datetime.now(UTC),
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Checks if the application can handle traffic (DB + Redis connectivity).",
)
async def readiness_check(
    db: AsyncSession = Depends(get_db),
) -> ReadinessResponse:
    """
    Readiness probe — can the app handle traffic?

    Checks connectivity to PostgreSQL and Redis.
    If this fails, the orchestrator should stop sending traffic
    but NOT restart the container.
    """
    checks: dict[str, str] = {}

    # Check PostgreSQL
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        logger.error("readiness_db_failed", error=str(e))

    # Check Redis
    try:
        redis = get_redis()
        await redis.ping()
        checks["redis"] = "connected"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
        logger.error("readiness_redis_failed", error=str(e))

    # Overall status
    all_healthy = all(v == "connected" for v in checks.values())

    return ReadinessResponse(
        status="ready" if all_healthy else "degraded",
        checks=checks,
        timestamp=datetime.now(UTC),
    )
