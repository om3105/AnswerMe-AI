"""
API v1 Router Aggregator

Collects all v1 endpoint routers into a single router
that is included in the main FastAPI app.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health

v1_router = APIRouter(prefix="/api/v1")

# Health check endpoints
v1_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

# Authentication endpoints
v1_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)
