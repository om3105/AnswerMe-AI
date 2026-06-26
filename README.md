<p align="center">
  <h1 align="center">🧠 AnswerMe AI</h1>
  <p align="center">
    <strong>Enterprise-Grade AI Knowledge Assistant</strong>
  </p>
  <p align="center">
    Built with FastAPI · React · PostgreSQL · Redis · Docker
  </p>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#api-documentation">API Docs</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Overview

**AnswerMe AI** is a production-ready AI Knowledge Assistant designed to demonstrate
enterprise-grade software engineering practices. The project is built in phases, starting
with a rock-solid foundation and progressively adding RAG, Agentic AI, MLOps, and
cloud deployment capabilities.

### Current Phase: Phase 1 — Foundation

Phase 1 focuses on building the software engineering backbone:

- ✅ Clean Architecture with SOLID principles
- ✅ JWT Authentication (access + refresh tokens)
- ✅ Async FastAPI with SQLAlchemy 2.0
- ✅ PostgreSQL + Redis infrastructure
- ✅ Docker Compose orchestration
- ✅ Structured logging and health checks
- ✅ React + Vite frontend with TypeScript

### Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Foundation (Auth, Docker, Architecture) | 🔨 In Progress |
| **Phase 2** | RAG Pipeline (Embeddings, Vector DB, Retrieval) | ⏳ Planned |
| **Phase 3** | Agentic AI (LangChain, Tool Use, Memory) | ⏳ Planned |
| **Phase 4** | MLOps (CI/CD, Monitoring, Model Registry) | ⏳ Planned |
| **Phase 5** | Cloud Deployment (AWS/GCP, Kubernetes, Terraform) | ⏳ Planned |

---

## Features

- 🔐 **JWT Authentication** — Secure access + refresh token pattern with bcrypt hashing
- 🏗️ **Clean Architecture** — Layered separation (API → Services → Repositories → Models)
- 🐳 **Dockerized** — Multi-stage builds, Docker Compose with 5 services
- 📊 **Health Checks** — Liveness, readiness, and detailed health probes
- 📝 **Structured Logging** — JSON-formatted logs with request tracing
- ⚡ **Fully Async** — Async SQLAlchemy, async Redis, ASGI server
- 🎨 **Modern Frontend** — React 19 + Vite, TypeScript, dark-mode glassmorphism UI
- 📖 **API Documentation** — Auto-generated Swagger UI and ReDoc

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Nginx (Reverse Proxy)               │
│                       :80 / :443                         │
├────────────────────────┬────────────────────────────────┤
│                        │                                │
│    /* → Frontend       │    /api/* → Backend            │
│                        │                                │
├────────────────────────┼────────────────────────────────┤
│                        │                                │
│   ┌──────────────┐     │   ┌──────────────────────┐     │
│   │  React+Vite  │     │   │     FastAPI           │     │
│   │  SPA Client  │     │   │  ┌────────────────┐  │     │
│   │  TypeScript  │─────┼──▶│  │  API Layer     │  │     │
│   └──────────────┘     │   │  │  (Routes)      │  │     │
│                        │   │  └───────┬────────┘  │     │
│                        │   │  ┌───────▼────────┐  │     │
│                        │   │  │  Service Layer │  │     │
│                        │   │  │  (Business)    │  │     │
│                        │   │  └───────┬────────┘  │     │
│                        │   │  ┌───────▼────────┐  │     │
│                        │   │  │  Repository    │  │     │
│                        │   │  │  (Data Access) │  │     │
│                        │   │  └───────┬────────┘  │     │
│                        │   └──────────┼──────────┘     │
│                        │              │                 │
├────────────────────────┼──────────────┼─────────────────┤
│                        │              │                 │
│   ┌──────────────┐     │   ┌──────────▼──────────┐     │
│   │   Redis 7    │     │   │   PostgreSQL 16     │     │
│   │  Cache/Rate  │     │   │   Users/Sessions    │     │
│   └──────────────┘     │   └─────────────────────┘     │
│                        │                                │
└────────────────────────┴────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19, Vite 6, TypeScript | Fast SPA with HMR, client-side routing |
| **Backend** | FastAPI, Python 3.14 | Async API framework |
| **ORM** | SQLAlchemy 2.0, Alembic | Database modeling, migrations |
| **Database** | PostgreSQL 16 | Primary data store |
| **Cache** | Redis 7 | Caching, rate limiting, sessions |
| **Auth** | JWT (PyJWT), bcrypt | Stateless authentication |
| **Proxy** | Nginx | Reverse proxy, TLS, load balancing |
| **Container** | Docker, Docker Compose | Containerization, orchestration |
| **Logging** | structlog | Structured JSON logging |
| **Testing** | pytest, Jest | Backend and frontend testing |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- [Git](https://git-scm.com/)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/om3105/AnswerMe-AI.git
cd AnswerMe-AI

# 2. Copy environment variables
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. Open the app
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
```

### Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev   # starts Vite dev server on http://localhost:5173
```

---

## Project Structure

```
AnswerMe-AI/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   ├── core/              # Config, security, logging
│   │   ├── db/                # Database setup & migrations
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access layer
│   │   └── main.py            # FastAPI entry point
│   ├── tests/                 # Test suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                  # React + Vite SPA
│   ├── src/
│   │   ├── pages/             # Page components (Login, Register, Dashboard)
│   │   ├── components/        # Reusable UI components
│   │   ├── lib/               # Utilities & API client
│   │   ├── hooks/             # Custom React hooks
│   │   ├── context/           # React Context providers (Auth)
│   │   └── types/             # TypeScript types
│   ├── Dockerfile
│   └── vite.config.ts
├── docker/                    # Docker configs (nginx, postgres)
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── docker-compose.yml
├── docker-compose.dev.yml
├── brain.md                   # 🧠 Learning journal
└── README.md
```

---

## API Documentation

Once running, interactive API docs are available at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/register` | Register a new user | ❌ |
| `POST` | `/api/v1/auth/login` | Login and get tokens | ❌ |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | 🔑 |
| `GET` | `/api/v1/auth/me` | Get current user | 🔑 |
| `GET` | `/api/v1/health` | Liveness probe | ❌ |
| `GET` | `/api/v1/health/ready` | Readiness probe | ❌ |
| `GET` | `/api/v1/health/detailed` | Detailed health | 🔑 |

---

## Environment Variables

See [`.env.example`](.env.example) for all required variables.

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens | *(required)* |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `ENVIRONMENT` | `development` / `staging` / `production` | `development` |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

**Om Chandrakant Deo**

- GitHub: [@om3105](https://github.com/om3105)

---

<p align="center">
  Built with ❤️ as an enterprise-grade AI engineering portfolio project
</p>
