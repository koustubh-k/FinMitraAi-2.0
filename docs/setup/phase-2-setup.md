# Phase 2 Setup Guide: Authentication + Market Data

This document provides a step-by-step guide to setting up the FinMitra 2.0 backend on a fresh development machine.

## Required Accounts
The following external accounts are required for this phase:
- **GitHub**: To clone the repository and participate in development.
- **Yahoo Finance**: No explicit account is required for the `yfinance` library, which relies on public APIs. If a different provider is configured later, an account for that provider (e.g., AlphaVantage, Finnhub) will be required.

## API Keys
Currently, the system defaults to using a mock provider or the `yfinance` provider, neither of which require an API key out-of-the-box. 

If you configure a different market data provider in the future:
- **Usage**: Used to authenticate with the market data provider to retrieve stock quotes and historical prices.
- **Is Mandatory?**: No, only if you switch `MARKET_DATA_PROVIDER` to a provider that requires one.
- **Where to obtain**: From the provider's developer dashboard.
- **Where to store**: Locally in `apps/api/.env`.
- **Environment Variable**: `MARKET_DATA_API_KEY=`
- **Never commit**: Never place real keys in `.env.example` or commit `.env` to Git.

## Environment Variables
Ensure the following variables are configured in `apps/api/.env` (use `apps/api/.env.example` as a template):

```env
# Database
DATABASE_URL=postgresql+psycopg://finmitra:finmitra@postgres:5432/finmitra

# Authentication
JWT_SECRET_KEY=your_generated_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30

# Market Data
MARKET_DATA_PROVIDER=yahoo
MARKET_DATA_API_KEY=
```

### Generating a JWT Secret Key
You must generate a strong random secret for the `JWT_SECRET_KEY`.

**On Windows (PowerShell):**
```powershell
[guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")
```

**On Linux/macOS (Bash):**
```bash
openssl rand -hex 32
```
Copy the output and set it as `JWT_SECRET_KEY` in your `.env` file. Do not invent a secret manually or use a weak password.

## API Key Safety
> [!CAUTION]
> **DO:**
> - store keys in `.env`
> - keep `.env` out of Git
> - use `.env.example` as a template
> - rotate compromised keys immediately
> 
> **DO NOT:**
> - commit API keys to version control
> - put keys in frontend code
> - put keys in GitHub issues/PRs
> - put keys in README
> - log API keys
> - hard-code API keys

## Step-by-Step Setup Procedure

1. **Pull latest code**
   ```bash
   git pull origin main
   ```
2. **Create `.env` file**
   ```bash
   cp apps/api/.env.example apps/api/.env
   ```
3. **Generate authentication secret**
   Generate a secret using the instructions above and paste it into `apps/api/.env` as `JWT_SECRET_KEY`.
4. **Start Docker services**
   ```bash
   docker-compose up -d postgres redis api
   ```
5. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```
6. **Start frontend (optional)**
   ```bash
   docker-compose up -d web
   ```
7. **Verify Tests**
   ```bash
   docker-compose exec api pytest
   ```

## Verification Checklist

- [ ] `.env` created
- [ ] JWT secret configured
- [ ] Market-data provider configured
- [ ] API key configured if required
- [ ] Database running
- [ ] Alembic migrations applied
- [ ] Backend running
- [ ] Registration works (`POST /api/v1/auth/register`)
- [ ] Login works (`POST /api/v1/auth/login`)
- [ ] `/auth/me` works (`GET /api/v1/auth/me`)
- [ ] Protected portfolio endpoint works
- [ ] Market quote endpoint works (`GET /api/v1/market/quote/RELIANCE`)
- [ ] Historical data endpoint works (`GET /api/v1/market/history/RELIANCE`)
- [ ] Tests pass
- [ ] No secrets tracked by Git

## Troubleshooting

### Database connection failure
- **Symptom**: `OperationalError: failed to resolve host 'postgres'` or similar.
- **Likely Cause**: The database is not running or the `DATABASE_URL` is configured for localhost instead of the `postgres` docker service.
- **Solution**: Ensure you are running commands inside the Docker network (e.g. `docker-compose exec api ...`) or change `postgres` to `127.0.0.1` in your `.env` if running locally without Docker.

### Invalid JWT Configuration
- **Symptom**: 401 Unauthorized errors continuously on valid logins.
- **Likely Cause**: `JWT_SECRET_KEY` is missing, too short, or differs between instances.
- **Solution**: Generate a proper 32-byte hex string and restart the API server.

### Provider Unavailable / Rate Limit
- **Symptom**: `ProviderUnavailableError` (HTTP 503) or `RateLimitError` (HTTP 429) when fetching market data.
- **Likely Cause**: Yahoo Finance IP rate-limiting, or the external service is down.
- **Solution**: Wait a few minutes and try again. For testing, you can change `MARKET_DATA_PROVIDER=mock` in `.env` to bypass external network dependencies.

### Migration Failure
- **Symptom**: `Target database is not up to date` or failure during `alembic upgrade head`.
- **Likely Cause**: Database state is corrupted or out of sync with migrations.
- **Solution**: If on a local dev environment, you can drop the database and recreate it, or wipe the postgres volume (`docker-compose down -v; docker-compose up -d postgres`).
