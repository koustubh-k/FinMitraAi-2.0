# FinMitra 2.0 Test Matrix

Last verified: 2026-09-02

## Automated Suites

| Area | Command | Result | Notes |
|---|---|---|---|
| Backend unit/API/provider tests | `cd apps/api && .venv/Scripts/python.exe -m pytest tests -q` | PASS | `84 passed`, `3 warnings`. |
| Frontend lint | `cd apps/web && npm run lint` | PASS | ESLint completed with no reported errors. |
| Frontend production build | `cd apps/web && npm run build` | PASS | Next.js generated 16 routes. |
| Browser smoke | `cd apps/web && npx playwright test` | PASS | Existing title test passed. |
| Docker stack | `docker compose up -d --build` and `docker compose ps` | PASS | `postgres`, `redis`, `api`, and `web` healthy. |
| Database migrations | `docker compose exec api alembic upgrade head` | PASS | Schema is current. |

## Feature Matrix

| # | Feature | Test | Expected | Actual | Status | Priority |
|---|---|---|---|---|---|---|
| 1 | Health | `GET /health` | 200 + database ok | 200 + database ok | PASS | LOW |
| 2 | Register | `POST /api/v1/auth/register` | 201 + user | 201 + user with first/last name | PASS | CRITICAL |
| 3 | Login | `POST /api/v1/auth/login` | 200 + tokens | 200 + access and refresh tokens | PASS | CRITICAL |
| 4 | Auth profile | `GET /api/v1/auth/me` | Authenticated user | Returned user data, no password hash | PASS | CRITICAL |
| 5 | Refresh token | Backend tests | New token or 401 for invalid/revoked token | Covered by pytest | PASS | CRITICAL |
| 6 | Logout | `POST /api/v1/auth/logout` | 200 + token revoked | Live smoke returned success | PASS | HIGH |
| 7 | Portfolio create | `POST /api/v1/portfolios/` | 201 + portfolio | Live smoke returned UUID portfolio | PASS | HIGH |
| 8 | Portfolio list | `GET /api/v1/portfolios/` | Own portfolios only | Live smoke returned created portfolio | PASS | CRITICAL |
| 9 | Transaction create | `POST /api/v1/portfolios/{id}/transactions` | 201 + transaction | Live smoke created AAPL BUY transaction | PASS | HIGH |
| 10 | Transactions list | `GET /api/v1/portfolios/{id}/transactions` | Transaction list | Live smoke returned 1 transaction | PASS | HIGH |
| 11 | Holdings | `GET /api/v1/portfolios/{id}/holdings` | Derived holdings | Live smoke returned 1 holding | PASS | HIGH |
| 12 | Portfolio summary | `GET /api/v1/portfolios/{id}/summary` | Financial totals | Returned market value, P&L, return percentage | PASS | CRITICAL |
| 13 | Allocation | `GET /api/v1/portfolios/{id}/allocation` | Position weights | Returned `positions` array | PASS | HIGH |
| 14 | Market quote | `GET /api/v1/market/quote/AAPL` | Quote payload | Returned price with nullable change fields | PASS | HIGH |
| 15 | Market history | `GET /api/v1/market/history/AAPL` | Historical data | Returned 22 data points | PASS | HIGH |
| 16 | Company profile | `GET /api/v1/market/company/AAPL` | Company profile | Returned Apple Inc. profile | PASS | MEDIUM |
| 17 | Financial metrics | `GET /api/v1/market/metrics/AAPL` | Metrics payload | Returned metrics response | PASS | MEDIUM |
| 18 | Provider fallback | Composite provider | Fall through to working provider | Logs show fallback to Yahoo after provider warnings | PASS | HIGH |
| 19 | Document upload | `POST /api/v1/documents/upload` | 201 + document metadata | Uploaded `smoke.txt` successfully | PASS | CRITICAL |
| 20 | Assistant SSE | `POST /api/v1/assistant/chat` | `text/event-stream` | Returned `status` and `complete` events | PASS | HIGH |
| 21 | Web root | `GET http://localhost:3000` | 200 | Returned 200 | PASS | HIGH |
| 22 | Playwright | `npx playwright test` | Browser smoke pass | 1 passed | PASS | MEDIUM |
| 23 | Frontend build | `npm run build` | TypeScript/build pass | Passed | PASS | HIGH |
| 24 | Frontend lint | `npm run lint` | ESLint pass | Passed | HIGH |
| 25 | Security | `.env` not tracked | No secrets committed | `.env` is ignored/untracked | PASS | CRITICAL |
| 26 | Security | Strong deployed secrets | No defaults in real environments | Local `.env` contains developer secrets; rotate if shared | WARN | CRITICAL |
| 27 | Persistence | Conversation history | Stored chat history | No conversation/message tables yet | GAP | HIGH |

## Known Gaps

- Frontend e2e coverage is still thin; only the title smoke test is automated.
- Document upload works live, but needs a dedicated backend test.
- Assistant SSE works live, but graceful failure cases for missing provider credentials need tests.
- Conversation and message persistence are not implemented.
- Market provider logs can show warnings for exhausted or unauthorized providers before Yahoo fallback succeeds.
