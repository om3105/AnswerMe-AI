"""
API v1 Router Aggregator

Collects all v1 endpoint routers into a single router
that is included in the main FastAPI app.

This keeps main.py clean — it only includes v1_router,
and this module handles wiring all sub-routers together.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

# Create the v1 router with a prefix
v1_router = APIRouter(prefix="/api/v1")

# Include endpoint routers
# Each endpoint module defines its own prefix and tags
v1_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

# Auth and user routers will be added in Step 5:
# v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# v1_router.include_router(users.router, prefix="/users", tags=["Users"])
