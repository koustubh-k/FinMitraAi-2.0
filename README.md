# FinMitra 2.0

> Enterprise-grade, evidence-first financial intelligence platform.

---

## Tech Stack Overview

- **Backend**: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (AsyncIO), Alembic, AsyncPG, Redis, HTTPX, Pytest, Ruff.
- **Frontend**: Next.js 14+ (App Router), TypeScript (Strict Mode), Tailwind CSS, **shadcn/ui** (accessible UI primitives) + **@tremor/react** (financial KPI cards, charts, and metrics dashboard).
- **Infrastructure**: Docker Compose, PostgreSQL 16 with `pgvector` extension (host port `5433`), Redis 7 (host port `6380`).
- **DevSecOps**: Gitleaks, Ruff, strict pre-commit hooks, isolated GitHub Actions CI pipeline.

---

## Monorepo Architecture

```
FinMitraAI/
├── apps/
│   ├── api/             # FastAPI backend with async database layer
│   └── web/             # Next.js frontend with shadcn/ui & Tremor
├── docs/                # Architectural, API, and setup documentation
├── infra/               # Container and deployment configurations
├── data/                # Dataset directories (raw, processed, seeds)
├── evals/               # Evaluation datasets, benchmarks, and results
├── scripts/             # Development and operational utility scripts
├── docker-compose.yml   # Postgres 5433 (pgvector) & Redis 6380
└── Makefile             # Centralized developer command orchestrator
```

---

## Prerequisites

- **Python**: 3.12+ (tested with Python 3.13)
- **Node.js**: 20+ LTS (tested with Node.js 24)
- **Docker & Docker Compose**: Installed and running

---

## Verified Development Commands

### 1. Infrastructure Management
```bash
# Start PostgreSQL (pgvector on 5433) and Redis (6380) in detached mode
docker compose up -d

# Check service status and health
docker compose ps

# Stop infrastructure (preserves persistent postgres_data volume)
docker compose down
```
> **Note**: Avoid `docker compose down -v` to prevent unintended deletion of local database data.

### 2. Backend (FastAPI & Database)
```bash
cd apps/api

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run linting and formatting checks
ruff check .
ruff format --check .

# Run database migrations
alembic current
alembic upgrade head

# Run unit test suite
pytest -v tests/unit/
```

### 3. Frontend (Next.js with shadcn/ui & Tremor)
```bash
cd apps/web

# Install dependencies
npm install

# Run ESLint checks
npm run lint

# Build production bundle
npm run build

# Start development server on port 3000
npm run dev
```

---

## Port Mappings

| Service | Container Port | Host Port | Notes |
| :--- | :--- | :--- | :--- |
| **PostgreSQL (pgvector)** | `5432` | `5433` | Image: `pgvector/pgvector:pg16` |
| **Redis** | `6379` | `6380` | Image: `redis:7-alpine` |
| **FastAPI Backend** | `8000` | `8000` | REST API & Health checks |
| **Next.js Web UI** | `3000` | `3000` | Client Dashboard |

---

## CI/CD Pipeline

Continuous Integration runs on GitHub Actions via `.github/workflows/ci.yml`:
- **Backend**: Python 3.12, dependency installation, Ruff lint/format check, zero-network unit tests.
- **Frontend**: Node.js 22 LTS, npm install, Next.js linting, Next.js production build.
