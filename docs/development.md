# Development Guide

## Prerequisites
- Docker Desktop
- Node.js 22 LTS
- Python 3.12

## Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url> FinMitraAi-2.0
   cd FinMitraAi-2.0
   ```

2. **Environment variables:**
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to include your specific API keys if needed.*

## Running the Application

We use Docker Compose to manage all services.

```bash
# Start all services in the background
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

After the containers are started, apply database migrations:

```bash
docker compose exec api alembic upgrade head
```

Local service URLs:

| Service | Host URL/Port | Notes |
|---|---|---|
| Web | `http://localhost:3000` | Next.js app |
| API | `http://localhost:8000` | FastAPI app and OpenAPI docs |
| PostgreSQL | `localhost:5433` | Maps to `5432` inside Docker |
| Redis | `localhost:6380` | Maps to `6379` inside Docker |

## Local Development (Without Docker for App Code)

If you prefer to run the API and Web locally (faster reload times):

### 1. Start Infrastructure only
```bash
docker compose up -d postgres redis
```

When running the API on the host, use host ports in your local environment:

```bash
DATABASE_URL=postgresql+psycopg://finmitra:finmitra@127.0.0.1:5433/finmitra
REDIS_URL=redis://127.0.0.1:6380/0
```

### 2. Run API
```bash
cd apps/api
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```
*API docs at http://localhost:8000/docs*

### 3. Run Web
```bash
cd apps/web
npm ci
npm run dev
```
*Web app at http://localhost:3000*

## Database Migrations (Alembic)

We use Alembic for database migrations. To run migrations, you can execute them directly inside the API container:

```bash
# Generate a new migration after changing models
docker compose exec api alembic revision --autogenerate -m "Description of changes"

# Apply migrations to the database
docker compose exec api alembic upgrade head
```

## Testing and Linting

```bash
# Backend
cd apps/api
.venv\Scripts\python.exe -m pytest tests -q
ruff check .

# Frontend
cd apps/web
npm run lint
npm run build
npx playwright install chromium
npx playwright test
```

Verified on 2026-09-02:

- Backend tests: `84 passed, 3 warnings`
- Frontend lint: passed
- Frontend production build: passed
- Playwright smoke test: passed
- Docker services: `postgres`, `redis`, `api`, and `web` healthy
