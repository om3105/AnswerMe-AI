"""
Service Layer — Use Cases (Business Logic)

This package contains the application's business rules.
In Clean Architecture, services are "Use Cases" — they orchestrate
the flow of data between repositories and the API layer.

Rules:
    1. Services NEVER import from api/ (no request/response objects)
    2. Services receive data as plain types or Pydantic models
    3. Services call repositories for data access (never raw SQL)
    4. Services contain ALL business rules (validation, authorization logic)
    5. Services are independently testable (mock the repository)

Services planned:
    auth_service.py → Registration, login, token management
    user_service.py → User CRUD operations (future)
"""
