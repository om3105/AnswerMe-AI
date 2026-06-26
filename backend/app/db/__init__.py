"""
Database Layer — Connection & Session Management

This package manages all database infrastructure:

    base.py      → SQLAlchemy declarative Base class (all models inherit from this)
    session.py   → Async session factory and engine configuration
    migrations/  → Alembic migration scripts (auto-generated and manual)

Key concepts:
    - Async engine: uses asyncpg driver for non-blocking PostgreSQL I/O
    - Session factory: creates scoped sessions per request (not per app)
    - Connection pooling: reuses connections instead of creating new ones
      (pool_size=5, max_overflow=10 is a good starting point)

Why separate from models/?
    - db/ = HOW we connect (infrastructure)
    - models/ = WHAT we store (domain entities)
    - This follows Interface Segregation Principle (SOLID "I")
"""
