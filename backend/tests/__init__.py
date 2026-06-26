"""
Test Suite — AnswerMe AI Backend

Structure:
    conftest.py    → Shared fixtures (test DB, test client, test user)
    unit/          → Unit tests (mock dependencies, fast, isolated)
    integration/   → Integration tests (real DB, real Redis, slower)

Testing strategy:
    - Unit tests mock the repository layer → test business logic in isolation
    - Integration tests use a real test database → test the full stack
    - All tests are async (pytest-asyncio)
    - Fixtures provide a clean database state per test (transaction rollback)
"""
