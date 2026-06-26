"""
API v1 Router Aggregator

This module collects all v1 endpoint routers into a single router
that is included in the main FastAPI app.

Pattern:
    main.py → includes v1_router
    v1/router.py → includes auth_router, health_router, users_router
    v1/endpoints/auth.py → defines auth routes
    v1/endpoints/health.py → defines health routes

This keeps main.py clean and allows each endpoint module to
define its own prefix and tags independently.
"""
