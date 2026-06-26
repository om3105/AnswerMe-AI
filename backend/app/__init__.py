"""
AnswerMe AI — Backend Application Package

This is the root package of the FastAPI backend application.
All sub-packages follow Clean Architecture principles:

    api/          → Interface Adapters (HTTP routes, dependency injection)
    core/         → Application Core (config, security, logging)
    db/           → Database Layer (session management, migrations)
    models/       → Entities (SQLAlchemy ORM models)
    schemas/      → DTOs (Pydantic request/response schemas)
    services/     → Use Cases (business logic)
    repositories/ → Data Access (repository pattern implementations)
"""

__version__ = "0.1.0"
