# Monorepo Architecture Overview: FinMitra 2.0

FinMitra 2.0 is an enterprise-grade, evidence-first financial intelligence platform engineered with a decoupled, modular monorepo architecture.

## Repository Layout

```
FinMitraAI/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated zero-network CI pipeline
├── apps/
│   ├── api/                     # Backend Service (FastAPI)
│   │   ├── alembic/             # Database migrations (async)
│   │   ├── app/
│   │   │   ├── api/v1/          # Versioned REST endpoints
│   │   │   ├── core/            # Core system configs and logging
│   │   │   ├── db/              # SQLAlchemy async engine, session, Base
│   │   │   ├── config.py        # Centralized Pydantic BaseSettings
│   │   │   └── main.py          # FastAPI app, CORS, error middleware
│   │   ├── tests/
│   │   │   └── unit/            # Isolated unit test suites
│   │   ├── alembic.ini          # Alembic configuration
│   │   ├── pyproject.toml       # Ruff and tool configuration
│   │   ├── pytest.ini           # Pytest discovery and options
│   │   └── requirements.txt     # Backend Python dependencies
│   └── web/                     # Frontend Service (Next.js 14)
│       ├── app/                 # App Router pages and layout
│       ├── components/
│       │   └── ui/              # shadcn/ui core components
│       ├── lib/
│       │   ├── config.ts        # Centralized NEXT_PUBLIC_API_URL
│       │   └── utils.ts         # Utility functions (cn)
│       ├── package.json         # Next.js, Tremor, Tailwind dependencies
│       ├── tailwind.config.ts   # Merged Tailwind + Tremor preset
│       └── tsconfig.json        # TypeScript strict configuration
├── data/
│   ├── raw/                     # Raw financial datasets (.gitkeep)
│   ├── processed/               # Processed documents & indices (.gitkeep)
│   └── seeds/                   # Baseline seed data (.gitkeep)
├── docs/
│   └── architecture/            # Architecture specifications
│       └── overview.md          # Monorepo structure and contracts
├── evals/                       # Evaluation benchmarks & metrics (.gitkeep)
├── infra/                       # Docker & deployment configs
├── scripts/                     # Operational & development scripts (.gitkeep)
├── .env.example                 # Safe environment variable templates
├── .gitignore                   # Strict security and cache exclusion rules
├── .pre-commit-config.yaml      # Gitleaks and Ruff pre-commit hooks
├── docker-compose.yml           # Containerized Postgres & Redis with custom ports
├── Makefile                     # Standardized developer workflows
└── README.md                    # Primary project documentation
```

## Key Architectural Decisions

1. **Decoupled Monorepo**:
   Frontend and backend operate independently with isolated dependency trees (`requirements.txt` vs. `package.json`), enabling separate CI execution and deployment targets.

2. **Frontend UI Architecture**:
   Combines **shadcn/ui** for accessible, headless primitives (buttons, dialogs, cards) with **@tremor/react** for financial metric cards, KPI blocks, and analytics charts.

3. **Backend Communication & CORS**:
   FastAPI applies `CORSMiddleware` as the outermost middleware to ensure CORS evaluation precedes authentication, preventing pre-flight OPTIONS 401 errors.

4. **Container Port Isolation**:
   Custom host port mappings (`PostgreSQL: 5433`, `Redis: 6380`) prevent collisions with default local PostgreSQL and Redis servers.
