"""
Test Configuration — Shared Fixtures

This module provides pytest fixtures used across all tests:
    - async_client: httpx.AsyncClient configured with the test app
    - db_session: async SQLAlchemy session with transaction rollback
    - test_user: a pre-created user for authenticated endpoint tests
    - redis_client: test Redis connection
    - settings_override: test-specific configuration

Each test runs in its own transaction that is rolled back after the test,
ensuring complete isolation between tests without manual cleanup.
"""

import pytest
