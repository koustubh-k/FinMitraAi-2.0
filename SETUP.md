# FinMitra 2.0 Web Setup

This project uses Next.js for the frontend, styled with Tailwind CSS and shadcn/ui. The web app is normally run together with the FastAPI backend through Docker Compose from the repository root.

## Prerequisites

- Node.js 22 LTS
- npm 10+
- Docker Desktop, when running the integrated stack

## Installation

1. **Install frontend dependencies:**
   Run this from `apps/web`:
   ```bash
   npm ci
   ```

2. **Environment Configuration:**
   Copy the `.env.example` to `.env.local` inside `apps/web` (if available), or set the environment variables manually. 
   ```bash
   # Required Environment Variables for Frontend
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

For Docker Compose, this is already supplied to the `web` service.

## Development

To start the development server for the web app:

```bash
cd apps/web
npm run dev
```

The app will be accessible at `http://localhost:3000`.

For the complete integrated app, run this from the repository root:

```bash
docker compose up -d --build
docker compose exec api alembic upgrade head
```

Current compose host ports:

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- PostgreSQL: `localhost:5433` mapped to container port `5432`
- Redis: `localhost:6380` mapped to container port `6379`

## Building for Production

To build the application for production deployment:

```bash
npm run build
```

The build output will be optimized and compiled into `.next/`. All TypeScript and linting checks are automatically verified during the build step.

## Deployment

The project is fully prepared for deployment on modern platforms like Vercel, Netlify, or any Docker/Node.js host.

- **Vercel**: Deploy the `apps/web` directory. Vercel automatically detects Next.js settings.
- **Docker**: The repository includes `apps/web/Dockerfile` and the root `docker-compose.yml`.

## Features Included
- **Auth**: Fully functional API client connected context.
- **Dashboard**: Home command center and portfolio tracking.
- **Assistant**: AI Assistant with streaming UI, tool results, and Markdown support.
- **Research**: Evidence-backed market research UI.
- **Settings**: Complete profile, preferences, and file intelligence uploading.

## Verified Checks

Last verified: 2026-09-02.

- `npm run lint` passed.
- `npm run build` passed.
- `npx playwright test` passed after installing the Playwright Chromium browser.
- Live browser entrypoint returned HTTP 200 at `http://localhost:3000`.
