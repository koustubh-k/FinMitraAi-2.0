# FinMitra 2.0

> Enterprise-grade, evidence-first financial intelligence platform.

## Architecture Overview

FinMitra 2.0 is designed as a decoupled monorepo:
- `apps/api`: Python 3.12+ FastAPI backend with asynchronous database and cache connections.
- `apps/web`: Next.js 14+ App Router frontend with TypeScript and Tailwind CSS.
- `packages/shared`: Shared types, schemas, and utilities.
- `infra/docker`: Infrastructure configurations including custom-port PostgreSQL and Redis.
- `evals/`: Evaluation benchmarks, datasets, and execution results.
- `docs/`: System architecture, API definitions, and research documentation.

## Local Infrastructure & Ports

Custom host port bindings prevent collisions with local standard services:
- **PostgreSQL (pgvector)**: Host port `5433` -> Container `5432`
- **Redis**: Host port `6380` -> Container `6379`
- **API**: Host port `8000` -> Container `8000`
- **Web**: Host port `3000` -> Container `3000`

## Quickstart

```bash
# Start containerized infrastructure
docker compose up -d

# Run backend tests
cd apps/api
pytest -v tests/unit/

# Run frontend checks
cd apps/web
npm run lint
npm run build
```
