# 🧠 AnswerMe AI — Brain (Learning Journal)

> This file is a living document. Every concept, decision, and lesson learned during
> the build of AnswerMe AI is recorded here. Think of it as your personal engineering
> textbook, written alongside production code.

---

## Table of Contents

1. [Step 1: Git & Version Control](#step-1-git--version-control)
2. [Step 2: Clean Architecture & SOLID](#step-2-clean-architecture--solid)
3. [Step 3: Docker & Containerization](#step-3-docker--containerization)
4. [Step 4: FastAPI & Backend Core](#step-4-fastapi--backend-core)
5. [Step 5: JWT Authentication](#step-5-jwt-authentication)
6. [Step 6: Health Checks & Observability](#step-6-health-checks--observability) *(upcoming)*
7. [Step 7: Next.js & Frontend](#step-7-nextjs--frontend) *(upcoming)*
8. [Step 8: Integration & DevOps](#step-8-integration--devops) *(upcoming)*

---

## Step 1: Git & Version Control

### 1.1 What is Git?

Git is a **distributed version control system (DVCS)** created by Linus Torvalds in 2005
for Linux kernel development. Unlike centralized systems (SVN, Perforce), every developer
has a complete copy of the repository history.

### 1.2 How Git Works Internally

Git is fundamentally a **content-addressable filesystem** — a key-value store where the
key is a SHA-1 hash of the content.

**Four object types:**

| Object | Purpose | Example |
|--------|---------|---------|
| **Blob** | Stores file contents (no filename!) | The raw bytes of `main.py` |
| **Tree** | Maps filenames → blobs/trees (like a directory) | `main.py → blob abc123` |
| **Commit** | Points to a tree + parent commit + metadata | Author, timestamp, message |
| **Tag** | Named pointer to a commit | `v1.0.0 → commit def456` |

```
commit → tree → blob (file content)
              → tree → blob (nested file)
              → blob (another file)
```

**Key insight:** Git doesn't store diffs — it stores **snapshots**. Each commit is a
complete snapshot of your project. Git uses **packfiles** and **delta compression** to
keep this efficient.

### 1.3 Why .gitignore Matters (Security!)

Files that should NEVER be committed:

| Category | Examples | Why |
|----------|----------|-----|
| **Secrets** | `.env`, `*.pem`, `*_secret*` | API keys, DB passwords — if leaked, your entire system is compromised |
| **Dependencies** | `node_modules/`, `venv/`, `__pycache__/` | Reproducible via lockfiles; bloats repo (node_modules can be 500MB+) |
| **Build artifacts** | `.next/`, `dist/`, `*.pyc` | Generated files — never version what you can regenerate |
| **IDE configs** | `.vscode/`, `.idea/` | Personal preferences — don't force on teammates |
| **OS files** | `.DS_Store`, `Thumbs.db` | Platform-specific junk |

**Real-world horror story:** In 2019, Uber's entire codebase was exposed because an
engineer committed AWS keys to a public GitHub repo. Automated bots scan GitHub for
secrets within seconds of a push.

### 1.4 Conventional Commits

A specification for writing standardized commit messages:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting (no logic change) |
| `refactor` | Code restructuring (no behavior change) |
| `test` | Adding/modifying tests |
| `chore` | Build scripts, CI, tooling |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |

**Why it matters:**
- Enables **automated changelog generation**
- Powers **semantic versioning** (feat = minor bump, fix = patch bump)
- Makes `git log` actually useful
- Required by many open-source projects

### 1.5 Branching Strategies

| Strategy | Best For | How It Works |
|----------|----------|--------------|
| **GitFlow** | Large teams, scheduled releases | `main` + `develop` + feature/release/hotfix branches |
| **Trunk-Based** | Small teams, CI/CD, microservices | Short-lived feature branches merged to `main` daily |
| **GitHub Flow** | Open source, SaaS | Feature branches → PR → merge to `main` → deploy |

**Our choice: GitHub Flow** — simple, CI/CD friendly, perfect for a project with 1-3 developers.

### 1.6 Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Committing `.env` files | Secrets in Git history forever (even after deletion!) | `.gitignore` + `git-secrets` pre-commit hook |
| Giant commits ("fix everything") | Impossible to review, revert, or bisect | Small, atomic commits with clear messages |
| Not using branches | Broken `main` = broken CI/CD = broken team | Always branch, always PR |
| Force-pushing to shared branches | Rewrites history for everyone | `--force-with-lease` if absolutely necessary |
| Committing `node_modules` | 500MB+ repo bloat | `.gitignore` — always |

### 1.7 Interview Questions

1. **Q: How does Git store data internally?**
   A: Git is a content-addressable filesystem using four object types: blobs (file content),
   trees (directory structure), commits (snapshots + metadata), and tags (named references).
   Objects are identified by SHA-1 hashes.

2. **Q: What's the difference between `git merge` and `git rebase`?**
   A: Merge creates a new merge commit preserving both histories. Rebase replays commits
   on top of another branch, creating a linear history. Use merge for shared branches,
   rebase for local cleanup.

3. **Q: If you accidentally commit a secret, how do you fix it?**
   A: Removing the file in a new commit is NOT enough — it's still in history. You need
   `git filter-branch` or `BFG Repo-Cleaner` to rewrite history, then force-push, then
   rotate all exposed credentials immediately.

4. **Q: What is a detached HEAD state?**
   A: HEAD normally points to a branch reference. Detached HEAD means HEAD points directly
   to a commit hash. Commits made in this state are "orphaned" unless you create a branch.

5. **Q: Explain the Git staging area (index).**
   A: The staging area is an intermediate zone between your working directory and the
   repository. `git add` moves changes to the staging area; `git commit` records the
   staged snapshot. This allows selective commits (committing parts of your changes).

### 1.8 Best Practices

- ✅ Write commit messages in **imperative mood** ("Add auth" not "Added auth")
- ✅ Keep commits **atomic** — one logical change per commit
- ✅ Use `.env.example` to document required variables (without values)
- ✅ Set up **pre-commit hooks** for linting and secret scanning
- ✅ Tag releases with **semantic versioning** (`v1.0.0`, `v1.1.0`)
- ✅ Write a comprehensive `README.md` — it's your project's front door
- ✅ Use `git blame` and `git bisect` for debugging — they're underused superpowers

### 1.9 Git Commit Message for This Step

```
chore: initialize repository with project foundation

- Add comprehensive .gitignore (Python, Node, Docker, IDE, secrets)
- Add README.md with project overview and architecture
- Add MIT LICENSE
- Add brain.md learning journal
- Configure conventional commit structure
```

---

*Next: Step 2 — Clean Architecture & SOLID Principles →*

---

## Step 2: Clean Architecture & SOLID Principles

### 2.1 What is Clean Architecture?

Clean Architecture is a software design philosophy introduced by **Robert C. Martin
(Uncle Bob)** in 2012. It organizes code into concentric layers where **dependencies
always point inward** — outer layers depend on inner layers, never the reverse.

```
┌─────────────────────────────────────────────────────┐
│              Frameworks & Drivers                   │  ← FastAPI, SQLAlchemy, Redis
│  ┌─────────────────────────────────────────────────┐│
│  │           Interface Adapters                    ││  ← Routes, Schemas, Repos
│  │  ┌─────────────────────────────────────────────┐││
│  │  │           Use Cases (Services)              │││  ← Business logic
│  │  │  ┌─────────────────────────────────────────┐│││
│  │  │  │          Entities (Models)               ││││  ← Core domain objects
│  │  │  └─────────────────────────────────────────┘│││
│  │  └─────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### 2.2 The Dependency Rule

> **Inner layers NEVER import from outer layers.**

This is the single most important rule. It means:
- `models/user.py` does NOT import from `api/` or `services/`
- `services/auth_service.py` does NOT import `FastAPI` or `Request`
- `repositories/user_repository.py` does NOT contain business rules

**Why?** If your business logic depends on FastAPI, you can never switch to Django
or test it without spinning up a web server. The Dependency Rule makes your core
logic framework-agnostic.

### 2.3 How Our Project Maps to Clean Architecture

| Layer | Directory | What Lives Here | Example |
|-------|-----------|----------------|---------|
| **Entities** | `models/` | ORM models, domain objects | `User` with columns and constraints |
| **Use Cases** | `services/` | Business logic, orchestration | `register_user()` — hash password, check uniqueness, save |
| **Interface Adapters** | `api/`, `schemas/`, `repositories/` | HTTP routes, DTOs, data access | `POST /auth/register` route handler |
| **Frameworks** | `core/`, `db/` | FastAPI, SQLAlchemy, Redis | Database engine, middleware, config |

**Data flow for user registration:**
```
HTTP Request → Route (api/) → Schema validation (schemas/)
            → Service (services/) → Repository (repositories/)
            → Database (db/) → Response Schema → HTTP Response
```

### 2.4 SOLID Principles (with Python Examples)

SOLID is a set of five design principles that make software **maintainable,
testable, and extensible**. Every principle is applied in our project.

---

#### S — Single Responsibility Principle (SRP)

> **A class should have only one reason to change.**

❌ **Bad — one class does everything:**
```python
class UserManager:
    def create_user(self, data):
        # Validates email format
        # Hashes password
        # Saves to database
        # Sends welcome email
        # Logs the event
        pass
```

✅ **Good — each class has one job:**
```python
class UserRepository:     # Only data access
    async def create(self, user_data): ...

class AuthService:        # Only business logic
    async def register_user(self, data): ...

class EmailService:       # Only email sending
    async def send_welcome(self, user): ...
```

**In our project:**
- `models/user.py` → defines the data structure (one reason to change: schema changes)
- `repositories/user_repository.py` → handles queries (one reason: query optimization)
- `services/auth_service.py` → enforces rules (one reason: business rules change)
- `api/v1/endpoints/auth.py` → handles HTTP (one reason: API contract changes)

---

#### O — Open/Closed Principle (OCP)

> **Software entities should be open for extension, closed for modification.**

❌ **Bad — modifying existing code to add features:**
```python
class NotificationService:
    def notify(self, user, channel):
        if channel == "email":
            send_email(user)
        elif channel == "sms":   # Must modify this method for every new channel!
            send_sms(user)
        elif channel == "slack":
            send_slack(user)
```

✅ **Good — extend via new classes, don't modify existing:**
```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    async def send(self, user, message): ...

class EmailChannel(NotificationChannel):
    async def send(self, user, message): ...

class SlackChannel(NotificationChannel):   # New channel = new class, no modification
    async def send(self, user, message): ...
```

**In our project:** The Repository pattern lets us swap PostgreSQL for MongoDB
by creating a new repository class without modifying the service layer.

---

#### L — Liskov Substitution Principle (LSP)

> **Subtypes must be substitutable for their base types without breaking behavior.**

❌ **Bad — subclass breaks the contract:**
```python
class Bird:
    def fly(self): return "flying"

class Penguin(Bird):
    def fly(self): raise Exception("Penguins can't fly!")  # Breaks the contract!
```

✅ **Good — proper abstraction:**
```python
class Bird(ABC):
    @abstractmethod
    def move(self): ...

class Eagle(Bird):
    def move(self): return "flying"

class Penguin(Bird):
    def move(self): return "swimming"
```

**In our project:** Any `Repository` subclass can replace the base repository
in the service layer without breaking behavior.

---

#### I — Interface Segregation Principle (ISP)

> **Clients should not be forced to depend on interfaces they don't use.**

❌ **Bad — fat interface:**
```python
class UserRepository:
    def create(self): ...
    def read(self): ...
    def update(self): ...
    def delete(self): ...
    def export_to_csv(self): ...      # Not every consumer needs this!
    def generate_report(self): ...    # Nor this!
```

✅ **Good — focused interfaces:**
```python
class ReadableRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id): ...

class WritableRepository(ABC):
    @abstractmethod
    async def create(self, data): ...
```

**In our project:** Schemas are split by purpose (UserCreate, UserResponse,
UserLogin) instead of one giant User schema. Each endpoint gets only the
fields it needs.

---

#### D — Dependency Inversion Principle (DIP)

> **High-level modules should not depend on low-level modules.
> Both should depend on abstractions.**

❌ **Bad — service directly creates its dependencies:**
```python
class AuthService:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # Hardcoded! Can't test without real DB
```

✅ **Good — dependencies are injected:**
```python
class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # Injected! Can pass a mock for testing

# In FastAPI:
async def get_auth_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)
```

**In our project:** FastAPI's `Depends()` mechanism is our DI container.
Routes receive services, services receive repositories, repositories receive
database sessions — all injected, all testable.

### 2.5 Monorepo vs. Polyrepo

| Approach | What It Means | Pros | Cons |
|----------|--------------|------|------|
| **Monorepo** | Frontend + Backend in one repo | Atomic commits, shared tooling, easier refactoring | CI complexity, permission boundaries |
| **Polyrepo** | Separate repos for frontend/backend | Independent deployments, clearer ownership | Coordination overhead, version drift |

**Our choice: Monorepo** — we're a small team, and having frontend + backend in
one repo means we can make atomic changes (e.g., update API + frontend in one commit)
and share types/schemas.

### 2.6 Why pyproject.toml Instead of requirements.txt

| Feature | `requirements.txt` | `pyproject.toml` |
|---------|-------------------|-----------------|
| Dependency groups (dev, test, prod) | Need multiple files | Built-in `[project.optional-dependencies]` |
| Tool configuration | Separate files (setup.cfg, pytest.ini) | All in one file |
| Build metadata | Needs setup.py | Declarative |
| PEP compliance | Informal | PEP 621 standard |
| Lock file support | `pip freeze` (fragile) | Works with `pip-tools`, `poetry`, `uv` |

### 2.7 Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Business logic in route handlers | Untestable, duplicated | Move to service layer |
| Importing FastAPI in services | Couples business logic to framework | Services use plain types/Pydantic |
| One giant `models.py` file | Hard to navigate, merge conflicts | One file per model |
| Skipping schemas (returning ORM models directly) | Exposes internal fields (hashed_password!) | Always use response schemas |
| Circular imports | Python crashes at import time | Follow dependency direction (inward only) |
| No `__init__.py` files | Python won't recognize packages | Every directory needs one |

### 2.8 Interview Questions

1. **Q: Explain Clean Architecture and the Dependency Rule.**
   A: Clean Architecture organizes code into concentric layers (Entities → Use Cases →
   Interface Adapters → Frameworks). The Dependency Rule states that dependencies only
   point inward — inner layers never know about outer layers. This makes the core
   business logic framework-agnostic and independently testable.

2. **Q: What does SOLID stand for? Give a real example of each.**
   A: Single Responsibility (one class, one job), Open/Closed (extend, don't modify),
   Liskov Substitution (subtypes are interchangeable), Interface Segregation (small,
   focused interfaces), Dependency Inversion (depend on abstractions, inject dependencies).

3. **Q: Why separate schemas from ORM models?**
   A: ORM models represent the database (contain hashed_password, internal IDs). Schemas
   represent the API contract (never expose sensitive fields). They have different shapes
   for different operations (Create vs. Response vs. Update).

4. **Q: What is the Repository Pattern and why use it?**
   A: Repository Pattern provides an abstraction over data access. Services call
   `repo.get_by_email()` instead of writing SQL. Benefits: testability (mock the repo),
   swappable storage (PostgreSQL today, MongoDB tomorrow), single responsibility
   (queries are centralized).

5. **Q: How does FastAPI's Depends() implement Dependency Injection?**
   A: `Depends()` declares that a route parameter should be resolved by calling a
   function. FastAPI calls that function, resolves its own dependencies recursively,
   and injects the result. This creates a dependency tree that's automatically managed
   and makes testing easy (override dependencies in tests).

### 2.9 Best Practices

- ✅ Follow the **Dependency Rule** — imports flow inward, never outward
- ✅ Keep route handlers **thin** — validate, delegate to service, return response
- ✅ Use **type hints everywhere** — they're documentation that the compiler checks
- ✅ One model/schema per file — easier to navigate and fewer merge conflicts
- ✅ Write **docstrings** for every module, class, and public function
- ✅ Name files by their domain concept (`user.py`), not by their technical role (`model1.py`)
- ✅ Use `__init__.py` to control public API of each package

### 2.10 Git Commit Message for This Step

```
chore(structure): add complete project structure with clean architecture

- Create backend package with layered architecture (api, core, db, models,
  schemas, services, repositories)
- Add pyproject.toml with all dependencies and tool configuration
- Create test suite structure (unit, integration, conftest)
- Add frontend placeholder (React + Vite, to be initialized in Step 7)
- Create Docker support directories (nginx, postgres)
- Add documentation placeholders (architecture.md, api.md)
- Add development scripts (setup.sh, seed.sh)
- Every module includes descriptive docstrings
```

---

*Next: Step 3 — Docker & Containerization →*

---

## Step 3: Docker & Containerization

### 3.1 What is Docker?

Docker is a **containerization platform** that packages your application and all its
dependencies into a standardized unit called a **container**. A container is like a
lightweight virtual machine, but instead of virtualizing hardware, it virtualizes the
operating system.

```
Traditional VM:              Docker Container:
┌───────────────┐            ┌───────────────┐
│   Your App    │            │   Your App    │
├───────────────┤            ├───────────────┤
│   Guest OS    │            │   Libraries   │
├───────────────┤            └───────┬───────┘
│  Hypervisor   │                    │
├───────────────┤            ┌───────┴───────┐
│   Host OS     │            │  Docker Engine│
├───────────────┤            ├───────────────┤
│   Hardware    │            │   Host OS     │
└───────────────┘            └───────────────┘
  ~1GB per VM                  ~50MB per container
  Minutes to start             Seconds to start
```

### 3.2 How Docker Works Internally

Docker uses three Linux kernel features:

| Feature | What It Does | Docker Use |
|---------|-------------|------------|
| **Namespaces** | Isolates processes, network, filesystem | Each container has its own PID 1, network stack, mount points |
| **cgroups** | Limits CPU, memory, I/O | `--memory 512m --cpus 1.5` |
| **Union Filesystem** | Layers images efficiently | Base image + your code = overlay, shared read-only layers |

### 3.3 Docker Image Layers

Every `RUN`, `COPY`, and `ADD` instruction creates a new **layer**:

```dockerfile
FROM python:3.12-slim    # Layer 1: base image (~120MB, shared)
RUN apt-get install gcc  # Layer 2: system deps (~50MB)
COPY pyproject.toml .    # Layer 3: dependency file (~1KB)
RUN pip install .        # Layer 4: Python deps (~200MB)
COPY ./app ./app         # Layer 5: your code (~500KB)
```

**Key insight: Docker caches layers.** If Layer 3 hasn't changed, Layers 1-3 are
reused from cache and only 4-5 are rebuilt. That's why we copy `pyproject.toml`
BEFORE copying source code — dependency installs are cached unless deps change.

### 3.4 Multi-Stage Builds

Why our Dockerfiles have two `FROM` statements:

```
Stage 1 (builder):                Stage 2 (production):
┌─────────────────────┐           ┌─────────────────────┐
│ Python 3.12-slim    │           │ Python 3.12-slim    │
│ gcc, libpq-dev      │  COPY →   │ libpq5 only         │
│ pip, wheel          │  venv     │ /opt/venv (deps)    │
│ All build tools     │           │ /app (your code)    │
│ ~800MB              │           │ ~150MB              │
└─────────────────────┘           └─────────────────────┘
```

Build tools (gcc, pip cache) stay in Stage 1 and are **discarded**.
The production image only contains what's needed to **run** the app.

### 3.5 Docker Compose

Docker Compose orchestrates **multiple containers** as a single application:

```yaml
services:
  backend:    # FastAPI container
  frontend:   # React SPA container
  postgres:   # Database container
  redis:      # Cache container
  nginx:      # Reverse proxy container
```

**Service discovery:** Compose creates a DNS entry for each service name.
The backend can reach PostgreSQL at hostname `postgres` — no IP addresses needed.

**Health checks & startup order:**
```yaml
depends_on:
  postgres:
    condition: service_healthy  # Wait for DB to be ready
```

### 3.6 Nginx as Reverse Proxy

Why not expose FastAPI directly to the internet?

| Without Nginx | With Nginx |
|--------------|------------|
| Each service needs its own port | Single port (80/443) for everything |
| No TLS termination | Handles HTTPS certificates |
| No load balancing | Distributes traffic across instances |
| App server handles static files (slow) | Nginx serves static files 50x faster |
| No request buffering | Buffers slow clients, protects backend |

Our routing rules:
```
/api/*     → backend:8000  (FastAPI)
/docs      → backend:8000  (Swagger UI)
/*         → frontend:80   (React SPA)
```

### 3.7 PostgreSQL vs. Alternatives

| Database | Type | Best For | Trade-off |
|----------|------|----------|----------|
| **PostgreSQL** | Relational (SQL) | Complex queries, ACID, JSON support | Heavier than SQLite |
| MySQL | Relational (SQL) | Simple apps, WordPress | Fewer advanced features |
| MongoDB | Document (NoSQL) | Unstructured data, prototyping | No ACID by default |
| SQLite | Embedded (SQL) | Single-user apps, testing | No concurrent writes |

**Why we chose PostgreSQL:**
- ACID compliance (transactions that either fully complete or fully rollback)
- Native JSON/JSONB support (useful for AI metadata in future phases)
- UUID generation extensions
- Battle-tested at every scale (Instagram, Spotify, Reddit)

### 3.8 Redis Use Cases

Redis is an in-memory data structure store. We use it for:

| Use Case | How | Example |
|----------|-----|--------|
| **Caching** | Store frequently accessed data | Cache user profiles for 5 minutes |
| **Rate Limiting** | Count requests per time window | 100 requests/minute per IP |
| **Session Store** | Store refresh tokens | Token → user_id mapping |
| **Pub/Sub** | Real-time messaging | Future: WebSocket notifications |

Why not just use PostgreSQL for everything?
- Redis: **sub-millisecond** reads (in-memory)
- PostgreSQL: **1-10ms** reads (disk-based)
- For rate limiting, that 100x difference matters at scale

### 3.9 Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Running as root in container | Container escape → root on host | `USER appuser` in Dockerfile |
| No `.dockerignore` | Sends `node_modules` (500MB) to build context | Add `.dockerignore` |
| `COPY . .` before `pip install` | Every code change rebuilds all deps | Copy deps file first, install, then copy code |
| Hardcoded passwords in Compose | Secrets in version control | Use `.env` file + env_file directive |
| No health checks | Orchestrator can't detect failures | `HEALTHCHECK` in Dockerfile |
| Exposing DB ports to host in prod | Direct DB access from internet | Only expose via internal network |
| Using `latest` tag | Builds are non-reproducible | Pin specific versions (`python:3.12-slim`) |

### 3.10 Interview Questions

1. **Q: What is the difference between a Docker image and a container?**
   A: An image is a read-only template (like a class). A container is a running
   instance of an image (like an object). You can create many containers from one image.

2. **Q: Explain multi-stage builds and why they're important.**
   A: Multi-stage builds use multiple `FROM` statements. Build tools stay in early
   stages; only runtime artifacts are copied to the final stage. This reduces image
   size by 60-80% and eliminates build dependencies from production.

3. **Q: How does Docker networking work in Compose?**
   A: Compose creates a bridge network and a DNS entry for each service name.
   Containers communicate by service name (e.g., `postgres:5432`). External access
   is only through explicitly published ports.

4. **Q: What's the difference between `COPY` and `ADD` in Dockerfile?**
   A: `COPY` copies files from build context. `ADD` does the same but also supports
   URLs and auto-extracts tar archives. Best practice: always use `COPY` unless you
   specifically need `ADD`'s extra features.

5. **Q: Why run containers as non-root?**
   A: If an attacker exploits a vulnerability, they're limited to the `appuser`
   account instead of having root access. Combined with read-only filesystems and
   dropped capabilities, this follows the principle of least privilege.

6. **Q: What are Docker health checks and why do they matter?**
   A: Health checks are commands that Docker runs periodically to verify a container
   is functioning correctly. Orchestrators (Docker Compose, Kubernetes) use them to
   determine startup order, auto-restart unhealthy containers, and route traffic only
   to healthy instances.

### 3.11 Best Practices

- ✅ Use **multi-stage builds** to minimize image size
- ✅ Run as **non-root user** (`USER appuser`)
- ✅ Add **`.dockerignore`** to exclude unnecessary files from build context
- ✅ **Pin image versions** (`python:3.12-slim` not `python:latest`)
- ✅ Copy **dependency files before source code** for layer caching
- ✅ Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`
- ✅ Use **health checks** for all services
- ✅ Use **named volumes** for persistent data
- ✅ Don't expose database/cache ports in production
- ✅ Use `--no-cache-dir` with pip to keep images small

### 3.12 Git Commit Message for This Step

```
feat(docker): add complete Docker infrastructure

- Add multi-stage Dockerfile for backend (non-root, health check)
- Add multi-stage Dockerfile for frontend (Vite build → Nginx serve)
- Add docker-compose.yml with 5 services (nginx, backend, frontend,
  postgres, redis)
- Add docker-compose.dev.yml with hot-reload and exposed ports
- Add Nginx reverse proxy config (production + development)
- Add PostgreSQL init script (UUID and pgcrypto extensions)
- Add .dockerignore files for both backend and frontend
```

---

*Next: Step 4 — FastAPI & Backend Core →*

---

## Step 4: FastAPI & Backend Core

### 4.1 What is FastAPI?

FastAPI is a modern, high-performance Python web framework built on top of
**Starlette** (ASGI toolkit) and **Pydantic** (data validation). Created by
Sebastián Ramírez in 2018.

Key features:
- **Automatic API documentation** (Swagger UI + ReDoc)
- **Type-based validation** via Pydantic
- **Async-first** with full `async/await` support
- **Dependency injection** built into the framework
- **Performance** comparable to Node.js and Go

### 4.2 FastAPI vs. Flask vs. Django

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Async support | Native | Via extensions | Django 4.1+ (partial) |
| Auto documentation | Built-in (OpenAPI) | Manual (flask-apispec) | Django REST Framework |
| Validation | Pydantic (built-in) | Manual / Marshmallow | DRF Serializers |
| ORM | Bring your own | Bring your own | Built-in (Django ORM) |
| Learning curve | Low | Very low | High |
| Performance | ~15,000 req/s | ~2,000 req/s | ~1,500 req/s |
| Best for | APIs, microservices | Simple apps, prototypes | Full-stack, CMS, admin |

**Why we chose FastAPI:** We're building an API-first application where
performance, validation, and documentation are critical.

### 4.3 ASGI vs. WSGI

```
WSGI (synchronous):          ASGI (asynchronous):
Request 1 ──┬── Process        Request 1 ──┬── Start
Request 2 ──┤   (blocked)     Request 2 ──┤   (concurrent)
Request 3 ──┘               Request 3 ──┘
             │                           │
         Waiting for DB           Event loop handles
         (thread blocked)         all 3 concurrently
```

- **WSGI** (Flask, Django): one thread per request. If a request waits for DB,
  the thread is blocked and can't serve other requests.
- **ASGI** (FastAPI): event loop handles many requests concurrently. While
  waiting for DB I/O, the event loop serves other requests.

For I/O-bound workloads (API → database → cache), async is 3-5x more efficient.

### 4.4 Pydantic v2 — Why It's Special

Pydantic v2 has a **Rust core** (pydantic-core) that makes validation
5-50x faster than v1:

```python
from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8)
    full_name: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()
```

Pydantic validates at runtime, catching bad data before it hits your database.

### 4.5 Async SQLAlchemy 2.0

SQLAlchemy 2.0 introduced native async support:

```python
# Old style (synchronous, blocking)
result = session.query(User).filter_by(email=email).first()

# New style (async, non-blocking)
result = await session.execute(select(User).where(User.email == email))
user = result.scalar_one_or_none()
```

**Connection Pooling** explained:
```
Without pool:                With pool:
Request → CREATE conn         Request → BORROW conn from pool
          QUERY                          QUERY
          DESTROY conn                   RETURN conn to pool
          (~50ms overhead)               (~0ms overhead)
```

Our settings:
- `pool_size=5`: 5 persistent connections always open
- `max_overflow=10`: up to 10 extra connections under load
- `pool_pre_ping=True`: test connections before use (catches stale connections)
- `pool_recycle=1800`: replace connections older than 30 minutes

### 4.6 Lifespan Events

FastAPI's lifespan context manager handles startup/shutdown:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before first request
    await init_db()
    await init_redis()
    yield  # ← App runs here
    # SHUTDOWN: runs after last response
    await close_redis()
    await close_db()
```

This replaces the deprecated `@app.on_event("startup")` pattern.

### 4.7 Middleware Execution Order

Middleware executes in **reverse registration order** (last registered = first executed):

```
Request → CORS → RequestID → Route Handler → RequestID → CORS → Response
```

Our middleware stack:
1. **CORS**: handles preflight `OPTIONS` requests and sets CORS headers
2. **RequestID**: generates UUID per request, attaches to logs and response

### 4.8 Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Using `app = FastAPI()` globally without factory | Can't create test instances | Use `create_app()` factory |
| Forgetting `async` on DB operations | Blocks the event loop | Always `await` database calls |
| Not setting `expire_on_commit=False` | Lazy-loading errors in async | Set it on sessionmaker |
| Hardcoding config values | Different per environment | Use Pydantic Settings |
| Not closing connections on shutdown | Connection pool leaks | Use lifespan events |
| Plain text logging in production | Can't parse, can't filter | Use structlog with JSON |

### 4.9 Interview Questions

1. **Q: What is the difference between ASGI and WSGI?**
   A: WSGI is synchronous (one thread per request). ASGI is asynchronous
   (event loop handles many concurrent requests). ASGI is superior for
   I/O-bound workloads because threads aren't blocked waiting for DB/network.

2. **Q: Explain connection pooling in databases.**
   A: Connection pooling reuses database connections instead of creating/destroying
   them per request. This eliminates the ~50ms overhead of TCP handshake + auth
   per query. Pool parameters (pool_size, max_overflow) control resource usage.

3. **Q: Why use structured logging over print statements?**
   A: Structured logs (JSON) are machine-parseable, filterable, and consistent.
   They work with log aggregation tools (ELK, Datadog). Print statements are
   unstructured, can't be filtered, and are lost in production.

4. **Q: What is FastAPI's dependency injection system?**
   A: FastAPI's `Depends()` declares that a parameter should be resolved by
   calling a function. Dependencies can depend on other dependencies, forming
   a tree. This decouples route handlers from infrastructure and makes testing
   trivial (override dependencies with mocks).

5. **Q: What are lifespan events and why are they important?**
   A: Lifespan events run code on application startup and shutdown. They're
   critical for initializing database connections, warming caches, and
   gracefully closing resources. FastAPI uses an async context manager pattern.

### 4.10 Best Practices

- ✅ Use the **app factory pattern** (`create_app()`) for testability
- ✅ Use **lifespan events** for startup/shutdown (not deprecated `on_event`)
- ✅ Set `expire_on_commit=False` on async sessions
- ✅ Use `pool_pre_ping=True` to detect stale connections
- ✅ Add **request ID middleware** for distributed tracing
- ✅ Use **custom exception classes** with consistent error responses
- ✅ Never expose stack traces to clients in error responses
- ✅ Suppress noisy third-party loggers (`uvicorn.access`, `sqlalchemy.engine`)

### 4.11 Git Commit Message for This Step

```
feat(backend): implement FastAPI core with async DB, Redis, and middleware

- Implement Pydantic Settings configuration (env vars, validation)
- Set up structured logging with structlog (JSON/console modes)
- Create async SQLAlchemy 2.0 session factory with connection pooling
- Add Redis async connection manager
- Implement JWT security utilities (password hashing, token ops)
- Add Request ID middleware for distributed tracing
- Create custom exception hierarchy with global handlers
- Build FastAPI app factory with lifespan events
- Wire v1 router with health check endpoints
- Implement liveness and readiness health probes
```

---

*Next: Step 5 — JWT Authentication →*

---

## Step 5: JWT Authentication

### 5.1 What is JWT?

JSON Web Token (JWT) is an open standard (RFC 7519) for securely transmitting
information between parties as a JSON object. A JWT consists of three parts
separated by dots:

```
header.payload.signature

eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMiLCJleHAiOjE2OTl9.signature_here
└────── Header ──────┘└────── Payload ─────┘└── Signature ─┘
```

| Part | Contains | Base64-encoded? | Encrypted? |
|------|----------|----------------|------------|
| **Header** | Algorithm (HS256), token type (JWT) | Yes | No |
| **Payload** | Claims (sub, exp, iat, custom) | Yes | No |
| **Signature** | HMAC-SHA256(header + payload, secret) | Yes | N/A |

> **Important:** JWT payload is NOT encrypted — it's only Base64-encoded.
> Anyone can decode it. The signature only ensures it hasn't been **tampered with**.
> Never put sensitive data (passwords, SSN) in a JWT.

### 5.2 Access Token + Refresh Token Pattern

```
Login:
  Client ─── email + password ───→ Server
  Client ─── access_token (30min) + refresh_token (7d) ▒── Server

API Call:
  Client ─── Authorization: Bearer <access_token> ───→ Server
  (valid? → return data)

Token Expired:
  Client ─── refresh_token ───→ Server
  Client ─── new access_token ▒── Server
```

**Why two tokens?**
- **Access token** (30 min): short-lived, sent with every API request
- **Refresh token** (7 days): long-lived, used ONLY to get new access tokens

If the access token is stolen, the attacker has only 30 minutes.
The refresh token is sent rarely and can be revoked.

### 5.3 Password Hashing — Why bcrypt?

| Algorithm | Time to Hash | Brute-force 8-char password | Verdict |
|-----------|-------------|----------------------------|--------|
| MD5 | ~1µs | Seconds | ❌ NEVER use |
| SHA-256 | ~1µs | Seconds | ❌ NEVER use |
| **bcrypt** | ~100ms | **Years** | ✅ Use this |
| Argon2 | ~100ms | **Years** | ✅ Modern alternative |

**Why bcrypt is slow ON PURPOSE:**
- bcrypt has a **cost factor** (default 12) → 2^12 = 4,096 iterations
- Each hash takes ~100ms → attacker can try only ~10 passwords/second
- Compare to SHA-256: attacker can try ~1 billion passwords/second

### 5.4 Our Auth Flow (Data Flow)

```
Register:
  Client → POST /auth/register {email, password, full_name}
         → UserCreate schema validates (Pydantic)
         → auth.py route handler (thin)
         → AuthService.register() (business logic)
           → Check email uniqueness (UserRepository)
           → Hash password (bcrypt)
           → Create user (UserRepository)
         → UserResponse schema (no hashed_password!)
         → 201 Created

Login:
  Client → POST /auth/login {email, password}
         → AuthService.authenticate()
           → Find user by email (UserRepository)
           → Verify password (bcrypt)
           → Check is_active
           → Generate access + refresh tokens (JWT)
         → Token response

Protected Endpoint:
  Client → GET /auth/me [Authorization: Bearer <token>]
         → get_current_user dependency
           → Extract token from header (OAuth2PasswordBearer)
           → Decode JWT (verify signature + expiration)
           → Fetch user from DB
           → Check is_active
         → UserResponse
```

### 5.5 Alembic — Database Migrations

Alembic manages database schema changes (like Git for your database):

```bash
# Generate a migration from model changes
alembic revision --autogenerate -m "create users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# See current migration state
alembic current
```

**Why not just create tables from models?**
- Can't track what changed between deployments
- Can't rollback a bad schema change
- Can't apply incremental changes to production
- Alembic generates up/down migrations for safe evolution

### 5.6 OWASP Authentication Best Practices

| Practice | Our Implementation |
|----------|-------------------|
| Hash passwords with bcrypt/Argon2 | ✅ `passlib[bcrypt]` |
| Enforce password complexity | ✅ Schema validator (8+ chars, upper, lower, digit) |
| Don't reveal if email exists on login failure | ✅ "Invalid email or password" |
| Use short-lived access tokens | ✅ 30-minute expiration |
| Validate token type (access vs. refresh) | ✅ Check `type` claim |
| Never store plain-text passwords | ✅ `hashed_password` column |
| Use HTTPS in production | ✅ Nginx TLS termination |

### 5.7 Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Storing plain-text passwords | One breach exposes all accounts | Use bcrypt |
| Using MD5/SHA for passwords | GPU can crack billions/second | Use bcrypt (intentionally slow) |
| Same error for "wrong password" vs "email not found" | Leaks which emails are registered | Generic "Invalid credentials" |
| No token expiration | Stolen token = permanent access | Short-lived access + refresh |
| JWT secret in source code | Anyone can forge tokens | Use env vars |
| Not validating token type | Refresh token used as access token | Check `type` claim |
| Returning hashed_password in API | Exposes hash to offline attack | Use response schemas |

### 5.8 Interview Questions

1. **Q: How does JWT work? Walk through the flow.**
   A: Client sends credentials → server validates → server creates JWT
   (header.payload.signature) → client stores token → client sends token
   in Authorization header → server validates signature and claims.

2. **Q: Why use bcrypt instead of SHA-256 for password hashing?**
   A: SHA-256 is designed to be FAST (~1µs). An attacker with a GPU can try
   billions of passwords per second. bcrypt is intentionally SLOW (~100ms)
   with an adaptive cost factor, making brute-force attacks computationally
   infeasible.

3. **Q: What's the purpose of the refresh token?**
   A: The access token is short-lived (30 min) and sent with every request.
   If stolen, damage is limited. The refresh token is long-lived (7 days)
   and used only to obtain new access tokens. This reduces the window of
   exposure while maintaining a good user experience.

4. **Q: What are database migrations and why are they important?**
   A: Migrations are version-controlled schema changes. They let you evolve
   the database incrementally, rollback bad changes, and apply the same
   changes consistently across dev/staging/production environments.

5. **Q: How does FastAPI's Depends() chain work for authentication?**
   A: `get_current_user` depends on `oauth2_scheme` (extracts token) and
   `get_auth_service` (provides the service). The auth service depends on
   `get_user_repository`, which depends on `get_db`. FastAPI resolves this
   entire chain automatically for each request.

### 5.9 Best Practices

- ✅ **Never store plain passwords** — always hash with bcrypt or Argon2
- ✅ **Use access + refresh token pattern** for secure sessions
- ✅ **Validate token type** in every token operation
- ✅ **Generic error messages** on auth failures (don't leak info)
- ✅ **Separate schemas** for input (UserCreate) and output (UserResponse)
- ✅ **Soft-delete users** (is_active flag) instead of hard-deleting
- ✅ **Use Alembic** for all schema changes (never raw SQL in production)
- ✅ **Pin JWT secrets** in environment variables, never in code

### 5.10 Git Commit Message for This Step

```
feat(auth): implement JWT authentication system

- Add User model with UUID PK, email, hashed_password, timestamps
- Create Pydantic schemas (UserCreate, UserLogin, UserResponse, Token)
- Implement UserRepository with async CRUD operations
- Build AuthService with register, authenticate, refresh, get_user
- Add auth endpoints (register, login, refresh, /me)
- Set up get_current_user dependency chain with OAuth2
- Configure Alembic for async migrations
- Add initial migration for users table
- Add email-validator dependency
```

---

*Next: Step 6 — Health Checks & Observability →*
