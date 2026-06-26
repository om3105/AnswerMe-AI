"""
API Layer — Interface Adapters

This package contains all HTTP route handlers organized by API version.
Routes are thin — they validate input, call services, and return responses.
No business logic should live here.

Structure:
    v1/endpoints/  → Individual route modules (auth, health, users)
    v1/router.py   → Aggregates all v1 endpoint routers
    deps.py        → Shared dependency injection functions
"""
