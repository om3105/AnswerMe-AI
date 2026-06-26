# 🧠 AnswerMe AI — Brain (Learning Journal)

> This file is a living document. Every concept, decision, and lesson learned during
> the build of AnswerMe AI is recorded here. Think of it as your personal engineering
> textbook, written alongside production code.

---

## Table of Contents

1. [Step 1: Git & Version Control](#step-1-git--version-control)
2. [Step 2: Clean Architecture & SOLID](#step-2-clean-architecture--solid) *(upcoming)*
3. [Step 3: Docker & Containerization](#step-3-docker--containerization) *(upcoming)*
4. [Step 4: FastAPI & Backend Core](#step-4-fastapi--backend-core) *(upcoming)*
5. [Step 5: JWT Authentication](#step-5-jwt-authentication) *(upcoming)*
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
