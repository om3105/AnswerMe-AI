"""
Repository Layer — Data Access

This package implements the Repository Pattern, providing an abstraction
over database operations. Repositories are the ONLY place where SQL/ORM
queries are written.

Why Repository Pattern?
    - Decouples business logic from data access
    - Services don't know if data comes from PostgreSQL, MongoDB, or a mock
    - Makes unit testing trivial: mock the repository, not the database
    - Single Responsibility: repositories handle queries, services handle rules

Rules:
    1. Repositories NEVER contain business logic
    2. Repositories return ORM models or None (never raise business exceptions)
    3. Repositories receive a session via dependency injection
    4. One repository per aggregate root (UserRepository for User model)

Repositories planned:
    user_repository.py → CRUD operations for User model
"""
