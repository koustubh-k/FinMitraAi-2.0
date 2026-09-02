# Frontend/Backend Integration Status

Date checked: 2026-09-02

This document tracks the current integration status between the Next.js frontend in `apps/web` and the FastAPI backend in `apps/api`.

## Current Test Status

| Area | Command / Check | Result | Notes |
|---|---|---|---|
| Docker build | `docker compose up -d --build` | PASS | API and web images built successfully. |
| Docker services | `docker compose ps` | PASS | `postgres`, `redis`, `api`, and `web` healthy. |
| Database migrations | `docker compose exec api alembic upgrade head` | PASS | Alembic completed against the compose database. |
| API health | `GET /health` | PASS | Returned `status: ok`, `database: ok`. |
| API tests | `cd apps/api && .venv/Scripts/python.exe -m pytest tests -q` | PASS | `84 passed`, `3 warnings`. |
| Frontend lint | `cd apps/web && npm run lint` | PASS | ESLint completed without reported errors. |
| Frontend build | `cd apps/web && npm run build` | PASS | Next.js production build completed. |
| Browser smoke | `cd apps/web && npx playwright test` | PASS | Existing title smoke test passed after installing Chromium. |
| Live integration smoke | Node fetch script against `localhost:8000` | PASS | Auth, portfolios, transactions, market data, upload, assistant SSE, and logout passed. |

## Runtime Endpoints

| Service | Host URL/Port | Container Port |
|---|---|---|
| Web | `http://localhost:3000` | `3000` |
| API | `http://localhost:8000` | `8000` |
| PostgreSQL | `localhost:5433` | `5432` |
| Redis | `localhost:6380` | `6379` |

PostgreSQL and Redis use offset host ports because another local Docker stack can commonly occupy `5432` and `6379`. Containers still communicate through the Docker service names and internal ports.

## Live Smoke Coverage

The live smoke test verified:

1. `GET /health`
2. `POST /api/v1/auth/register` with `first_name` and `last_name`
3. `POST /api/v1/auth/login`
4. `GET /api/v1/auth/me`
5. `POST /api/v1/portfolios/`
6. `GET /api/v1/portfolios/`
7. `POST /api/v1/portfolios/{portfolio_id}/transactions`
8. `GET /api/v1/portfolios/{portfolio_id}/transactions`
9. `GET /api/v1/portfolios/{portfolio_id}/holdings`
10. `GET /api/v1/portfolios/{portfolio_id}/summary`
11. `GET /api/v1/portfolios/{portfolio_id}/allocation`
12. `GET /api/v1/market/quote/AAPL`
13. `GET /api/v1/market/history/AAPL`
14. `GET /api/v1/market/company/AAPL`
15. `GET /api/v1/market/metrics/AAPL`
16. `POST /api/v1/documents/upload`
17. `POST /api/v1/assistant/chat`
18. `POST /api/v1/auth/logout`

## Current API Coverage Matrix

| API Route | Backend Status | Frontend Coverage | Integration Status | Notes |
|---|---:|---|---|---|
| `GET /health` | Working | API-only | PASS | Used by health checks. |
| `POST /api/v1/auth/register` | Working | `/register` | PASS | Names are accepted and returned. |
| `POST /api/v1/auth/login` | Working | `/login` | PASS | Returns access and refresh tokens. |
| `POST /api/v1/auth/refresh` | Working/tested | Client support pending | PARTIAL | Backend test coverage exists. |
| `POST /api/v1/auth/logout` | Working/tested | UI action pending | PARTIAL | Live API logout passed. |
| `GET /api/v1/auth/me` | Working | `AuthProvider` | PASS | Returns profile including names. |
| `POST /api/v1/users/` | Exists | No UI | API-only | Overlaps with `/auth/register`; decide admin-only vs removal later. |
| `GET /api/v1/users/{user_id}` | Exists | No UI | API-only | Could support profile/settings later. |
| `GET /api/v1/portfolios/` | Working | `/portfolio` | PASS | Live smoke verified. |
| `POST /api/v1/portfolios/` | Working | `/portfolio` | PASS | Live smoke verified. |
| `POST /api/v1/portfolios/{portfolio_id}/transactions` | Working | Portfolio detail | PASS | Live smoke verified. |
| `GET /api/v1/portfolios/{portfolio_id}/transactions` | Working | Portfolio detail | PASS | Live smoke verified. |
| `GET /api/v1/portfolios/{portfolio_id}/holdings` | Working | Portfolio detail | PASS | Live smoke verified. |
| `GET /api/v1/portfolios/{portfolio_id}/summary` | Working | Portfolio detail | PASS | Uses `market_value`, `total_pnl`, and `return_percentage`. |
| `GET /api/v1/portfolios/{portfolio_id}/allocation` | Working | Portfolio detail | PASS | Uses `allocation.positions`. |
| `GET /api/v1/market/quote/{symbol}` | Working | `/research` | PASS | Handles nullable `previous_close` and `day_change_percent`. |
| `GET /api/v1/market/history/{symbol}` | Working | `/research` | PASS | Live smoke returned historical points. |
| `GET /api/v1/market/company/{symbol}` | Working | `/research` | PASS | Live smoke returned company profile. |
| `GET /api/v1/market/metrics/{symbol}` | Working | `/research` | PASS | Live smoke returned metrics payload. |
| `GET /api/v1/research/` | Working but deprecated | No primary UI | API-only | Keep only while migration path needs it. |
| `POST /api/v1/assistant/chat` | Working | `/assistant` | PASS | SSE response returned `status` and `complete` events. |
| `POST /api/v1/documents/upload` | Working | `/settings/files` and upload flow | PASS | Requires embedding provider key in API env. |

## Known Follow-Up Work

- Add broader Playwright coverage for register/login, research tabs, portfolio create/detail, upload, and assistant streaming.
- Add backend tests for `/api/v1/documents/upload`.
- Add assistant tests for graceful provider/key failures.
- Decide whether `/api/v1/users/` should remain public, become admin-only, or be removed in favor of `/auth/register`.
- Add refresh-token handling in the web client.
- Add persistent conversation/message tables if chat history is a product requirement.
- Rotate any local provider keys that have been shared outside the developer machine.

## Definition Of Done

The current integrated local stack meets the local integration definition of done:

- `docker compose up -d --build` starts all services healthy.
- `docker compose exec api alembic upgrade head` succeeds.
- `cd apps/api && .venv/Scripts/python.exe -m pytest tests -q` passes.
- `cd apps/web && npm run lint` passes.
- `cd apps/web && npm run build` passes.
- `cd apps/web && npx playwright test` passes.
- Live smoke confirms auth, portfolio, market, assistant SSE, upload, and logout routes.
