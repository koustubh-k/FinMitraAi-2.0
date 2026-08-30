# Phase 3 Setup Guide

## Requirements
- Python 3.12+
- PostgreSQL
- FinMitra 2.0 Backend Architecture (Phase 0-2 completed)

## Step 1: Database Migration
Phase 3 introduces `transactions` and `holdings` tables.
Apply the Alembic migrations inside the Docker container:

```bash
docker-compose exec api alembic upgrade head
```

## Step 2: Testing
Verify that all unit and integration tests pass successfully. Tests check authentication, market data integration, and the newly added deterministic financial engine endpoints.

```bash
docker-compose exec -e PYTHONPATH=/app api pytest
```

You should expect the suite (including `test_financial_engine.py` and `test_financial.py`) to pass.

## Step 3: Verify Endpoints
You can verify the Phase 3 implementation via Swagger UI (`http://localhost:8000/docs`).

1. Log in via `POST /api/v1/auth/login`.
2. Create a portfolio via `POST /api/v1/portfolios/`.
3. Add a transaction via `POST /api/v1/portfolios/{id}/transactions` (e.g. `BUY` a quantity of `TCS`).
4. Retrieve the portfolio summary via `GET /api/v1/portfolios/{id}/summary`. 
5. You should see realized P&L, unrealized P&L, cost basis, and total return properly formatted using Decimals.
