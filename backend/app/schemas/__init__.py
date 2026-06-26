"""
Pydantic Schemas — Data Transfer Objects (DTOs)

This package contains Pydantic models for request/response validation.
In Clean Architecture, these are at the boundary between layers.

Why separate from ORM models?
    - ORM models = database representation (has hashed_password)
    - Schemas = API representation (never exposes hashed_password)
    - Different shapes: UserCreate has 'password', UserResponse does not
    - Validation rules differ: API needs email format check, DB doesn't care

Naming convention:
    - UserCreate   → request body for registration
    - UserLogin    → request body for login
    - UserResponse → response body (safe, no sensitive data)
    - UserInDB     → internal model with hashed_password (never returned)
    - Token        → JWT token response
    - TokenPayload → decoded JWT payload
"""
