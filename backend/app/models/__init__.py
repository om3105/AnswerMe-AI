"""
ORM Models — Domain Entities

This package contains SQLAlchemy ORM models representing database tables.
In Clean Architecture, these are the "Entities" — the core business objects.

Each model:
    - Inherits from Base (app.db.base)
    - Defines table name, columns, relationships, and constraints
    - Uses type hints for all columns (SQLAlchemy 2.0 mapped_column style)

Models planned:
    user.py → User account (email, hashed_password, is_active, roles)

Principles:
    - Models are plain data containers — NO business logic here
    - Business rules live in services/ (Use Cases layer)
    - This follows Single Responsibility Principle (SOLID "S")
"""
