"""
API v1 — Version 1 Router Package

API versioning strategy: URL-based (/api/v1/...)
This allows us to evolve the API without breaking existing clients.

When v2 is needed:
    1. Create app/api/v2/ package
    2. Include it in main.py alongside v1
    3. Deprecate v1 endpoints with response headers
"""
