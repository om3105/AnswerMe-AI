# ==============================
# AnswerMe AI — Backend Dockerfile
# ==============================
# Multi-stage build for minimal production image.
#
# Stage 1 (builder): Install dependencies in a virtual environment
# Stage 2 (production): Copy only the venv + app code into a slim image
#
# Why multi-stage?
#   - Build tools (gcc, pip cache) stay in Stage 1 → never reach production
#   - Final image is ~150MB instead of ~800MB
#   - Smaller image = faster pulls, smaller attack surface
#
# Usage:
#   docker build -t answerme-backend .
#   docker run -p 8000:8000 answerme-backend

# ──────────────────────────────
# Stage 1: Builder
# ──────────────────────────────
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered output
# PYTHONDONTWRITEBYTECODE: no .pyc files (smaller image, cleaner logs)
# PYTHONUNBUFFERED: print() and logs appear immediately (critical for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install system dependencies required for building Python packages
# - gcc: needed to compile C extensions (e.g., bcrypt, asyncpg)
# - libpq-dev: PostgreSQL client library headers (needed by asyncpg)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
# Why venv in Docker? It isolates our deps from system Python,
# making the copy to Stage 2 clean and predictable
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only dependency files first (Docker layer caching optimization)
# If pyproject.toml hasn't changed, Docker reuses this cached layer
# instead of re-installing all dependencies — saves minutes on rebuilds
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# ──────────────────────────────
# Stage 2: Production
# ──────────────────────────────
FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install only runtime dependencies (no build tools)
# libpq5: PostgreSQL client library (runtime only, no headers)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
# Why? If the app is compromised, the attacker only has 'appuser' privileges,
# not root. This is a production security best practice.
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY ./app ./app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Health check — Docker and orchestrators use this to determine container health
# --fail: curl returns exit code 22 on HTTP errors (4xx, 5xx)
# --interval: check every 30 seconds
# --timeout: fail if no response in 10 seconds
# --retries: mark unhealthy after 3 consecutive failures
# --start-period: wait 40 seconds before first check (app startup time)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl --fail http://localhost:8000/api/v1/health || exit 1

# Run the application with uvicorn
# --host 0.0.0.0: listen on all interfaces (required in Docker)
# --port 8000: application port
# --workers 1: single worker (scale via Docker replicas, not workers)
# --log-level info: production log level
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
