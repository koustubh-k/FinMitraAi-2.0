# FinMitra AI 2.0 - Unified Setup Guide

This guide covers the complete setup for the FinMitra AI 2.0 platform, including the foundation, backend API, multi-agent AI framework, market data integrations, and observability.

Last verified: 2026-09-02.

## Prerequisites

Ensure the following are installed on your development machine:

| Tool              | Minimum Version | Purpose                       |
| ----------------- | --------------- | ----------------------------- |
| **Git**           | 2.40+           | Version control               |
| **Docker Desktop**| 4.25+           | Container runtime             |
| **Node.js**       | 22 LTS          | Frontend toolchain            |
| **Python**        | 3.12+           | Backend runtime (optional for local dev) |
| **npm**           | 10+             | Node package manager          |

> [!TIP]
> On Windows, use **PowerShell 7+** for best compatibility with the commands in this guide.

## Required Accounts & API Keys

To use all features of the application, you need some external API keys.

| Service          | Required? | Purpose                                    |
| ---------------- | --------- | ------------------------------------------ |
| **LLM Provider** | Yes       | Powers the AI agents (e.g., Groq, Gemini)  |
| **LangSmith**    | Optional  | Observability and tracing                  |
| **Market Data**  | Optional  | `yahoo` and `duckduckgo` are free without keys. Keys needed for AlphaVantage, Finnhub, etc. |
| **Embeddings**   | Required for document upload/RAG | Configure `GOOGLE_API_KEY` or `GEMINI_API_KEY` when using the default Gemini embeddings. |

## 1. Initial Setup

### Clone the Repository

```bash
git clone <repo-url> FinMitraAi-2.0
cd FinMitraAi-2.0
```

### Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and configure the required settings:

#### Authentication Secret
Generate a strong secret key for JWT authentication.
- **Windows (PowerShell):** `[guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")`
- **Linux/macOS:** `openssl rand -hex 32`

Paste this into `JWT_SECRET_KEY`.

#### LLM Provider Configuration
FinMitra supports multiple LLMs. We recommend Groq (fastest) or Gemini (large context).
Set `LLM_PROVIDER`, `LLM_MODEL`, and the corresponding API key (e.g., `GROQ_API_KEY`, `GEMINI_API_KEY`).

#### Market Data Providers
Set `MARKET_DATA_PROVIDER=yahoo,duckduckgo` or configure keys for other providers like `ALPHA_VANTAGE_API_KEY`.

#### Observability (LangSmith) - Optional
If you have a LangSmith account, set `LANGCHAIN_TRACING_V2=true` and provide your `LANGCHAIN_API_KEY`.

> [!CAUTION]
> **DO NOT commit your `.env` file to version control.** It contains sensitive API keys and secrets.

## 2. Infrastructure & Services Setup

We use Docker Compose to run the PostgreSQL database (with pgvector for semantic search) and Redis.

Current host ports are intentionally offset to avoid conflicts with other local stacks:

| Service | Host URL/Port | Container Port |
| ------- | ------------- | -------------- |
| Web | `http://localhost:3000` | `3000` |
| API | `http://localhost:8000` | `8000` |
| PostgreSQL | `localhost:5433` | `5432` |
| Redis | `localhost:6380` | `6379` |

```bash
# Start the database and cache
docker compose up -d postgres redis
```

Wait a few seconds for the services to become healthy, then verify:
```bash
docker compose ps
```

## 3. Application Setup

You can run the API and Frontend via Docker or locally for development.

### Option A: Using Docker (Recommended)

1. **Start the API and Web services:**
   ```bash
   docker compose up -d --build api web
   ```

2. **Run database migrations:**
   ```bash
   docker compose exec api alembic upgrade head
   ```
   This creates all required tables (users, portfolios, transactions, holdings, and vector documents).

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Option B: Local Development

1. **Run Database Migrations (Local):**
   ```bash
   cd apps/api
   python -m venv .venv
   # Activate venv: .venv\Scripts\activate (Windows) OR source .venv/bin/activate (Linux/Mac)
   pip install -r requirements.txt -r requirements-dev.txt
   ```
   
   *Note: when running API code on the host, set `DATABASE_URL` to `postgresql+psycopg://finmitra:finmitra@127.0.0.1:5433/finmitra` and `REDIS_URL` to `redis://127.0.0.1:6380/0`. Inside Docker, the compose file overrides these to the service names `postgres` and `redis`.*
   
   ```bash
   alembic upgrade head
   ```

2. **Start the API:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Start the Frontend:**
   ```bash
   cd ../web
   npm ci
   npm run dev
   ```

## 4. Using the Platform

### Creating an Account
The Assistant API and Portfolio API require authentication.

1. **Register a user:**
   `POST http://localhost:8000/api/v1/auth/register`
   Body: `{"email": "user@example.com", "password": "yourpassword"}`

2. **Login to obtain JWT token:**
   `POST http://localhost:8000/api/v1/auth/login`

### Uploading Documents

Document ingestion is available through `POST /api/v1/documents/upload`. The route requires a bearer token and accepts `pdf`, `txt`, and `csv` files as multipart form data under the `file` field.

The upload flow depends on the embedding provider configuration. With the default Gemini embeddings, make sure `GOOGLE_API_KEY` or `GEMINI_API_KEY` is available to the API service. Docker Compose loads `.env` into the API container.

### Using the Assistant

The unified Assistant API (`POST /api/v1/assistant/chat`) acts as a Supervisor and routes to:
- **Research Agent:** For company analysis, risks, and RAG document search.
- **Portfolio Agent:** For user investments, P&L, and allocations (requires auth).
- **Education Agent:** For explaining financial concepts.
- **General Agent:** For conversational fallback.

Test it via UI at `http://localhost:3000/assistant` or via curl (make sure to pass your JWT Token in the Authorization header).

## 5. Security & Observability Features

- **Prompt Injection Defense:** Agents treat user context as untrusted.
- **Rate Limiting:** Global limit of 60 req/min, Assistant limit of 10 req/min (using `slowapi`).
- **Structured Logging:** Includes `X-Request-ID` and execution times in traces.
- **MCP Server:** A FastMCP server is available at `apps/api/app/mcp_server.py` for external tools. You can run it via `python -m app.mcp_server`.

## Troubleshooting

- **Database Connection Refused / Cannot Resolve Host 'postgres':**
  If running tests or migrations outside Docker, ensure `DATABASE_URL` points to `127.0.0.1` rather than the Docker service name `postgres`.
- **401 Unauthorized from Assistant API:**
  Ensure you have obtained a valid JWT and passed it in the Authorization header.
- **LLM Agent Routing Issues / All queries go to General:**
  Ensure your LLM provider supports structured output well (Groq/Gemini recommended). Check logs for LLM connection errors.
- **Rate Limit Errors (429):**
  If testing heavily, you may hit the 10 req/min Assistant limit. Wait a minute and try again.
- **Document upload returns embedding API key error:**
  Ensure `.env` contains `GOOGLE_API_KEY` or `GEMINI_API_KEY`, then recreate the API container with `docker compose up -d api`.
- **Host port 5432 or 6379 is already in use:**
  This project maps PostgreSQL to host port `5433` and Redis to host port `6380`; keep host-side tools pointed at those ports.
