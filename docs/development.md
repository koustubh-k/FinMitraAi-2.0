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

## Local Development (Without Docker for App Code)

If you prefer to run the API and Web locally (faster reload times):

### 1. Start Infrastructure only
```bash
docker compose up -d postgres redis
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

## Testing and Linting

```bash
# Backend
cd apps/api
pytest
ruff check .

# Frontend
cd apps/web
npm run lint
```
