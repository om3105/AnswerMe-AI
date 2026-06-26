-- ==============================
-- AnswerMe AI — PostgreSQL Initialization Script
-- ==============================
-- This script runs ONCE when the PostgreSQL container is first created.
-- It sets up the database, extensions, and initial configuration.
--
-- How it works:
--   Docker's postgres image auto-executes .sql files found in
--   /docker-entrypoint-initdb.d/ on first startup (only if the
--   data directory is empty).
--
-- Note: The database and user are already created by POSTGRES_DB and
-- POSTGRES_USER environment variables. This script adds extensions
-- and any additional setup.

-- ──────────────────────────────
-- Extensions
-- ──────────────────────────────

-- UUID generation: used for primary keys instead of auto-increment integers
-- Why UUIDs over integers?
--   - No sequential guessing (security)
--   - Safe for distributed systems (no central ID authority)
--   - Can be generated client-side
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pgcrypto: additional cryptographic functions
-- Used for: gen_random_uuid() (preferred over uuid_generate_v4())
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ──────────────────────────────
-- Schema setup
-- ──────────────────────────────
-- Note: Tables are managed by Alembic migrations, not this script.
-- This script only handles database-level configuration that must
-- exist before the application starts.

-- Verify extensions are installed
SELECT 'Database initialized successfully' AS status;
SELECT extname, extversion FROM pg_extension WHERE extname IN ('uuid-ossp', 'pgcrypto');
