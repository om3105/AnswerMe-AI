"""
Async Database Session Factory

This module creates and manages the async SQLAlchemy engine and session.

Components:
    - async_engine: AsyncEngine configured with connection pool settings
    - AsyncSessionLocal: sessionmaker bound to the async engine
    - get_db(): async generator that yields a session and auto-commits/rollbacks

Connection pooling parameters:
    - pool_size: number of persistent connections (default: 5)
    - max_overflow: extra connections allowed under load (default: 10)
    - pool_timeout: seconds to wait for a connection (default: 30)
    - pool_recycle: seconds before a connection is recycled (default: 1800)

Why async?
    - Database I/O is the #1 bottleneck in web applications
    - Async allows the event loop to handle other requests while waiting for DB
    - With asyncpg, we get 3-5x throughput vs. synchronous psycopg2
"""
