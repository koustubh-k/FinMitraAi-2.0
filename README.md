# FinMitra 2.0

### Evidence-First Financial Intelligence Platform

FinMitra is an open-source financial intelligence platform designed to help users research companies, understand financial information, analyze portfolios, and learn financial concepts through evidence-grounded AI.

The project is being rebuilt from the ground up with a focus on:

* **Evidence-first AI**
* **Deterministic financial calculations**
* **Agentic workflows**
* **Explainability and citations**
* **Safety and responsible AI**
* **Evaluation-driven development**
* **Production-grade backend engineering**
* **Open-source and reproducible development**

> **Status:** 🚧 Under active development
> **Current milestone:** Phase 2 (Authentication) & Phase 3 (Market Data) Completed

---

## Why FinMitra?

Financial information is distributed across market data, company filings, financial statements, news, and other sources.

Traditional financial applications provide data but often lack contextual explanations.

General-purpose AI assistants can explain financial concepts, but may:

* hallucinate financial information
* use outdated knowledge
* provide calculations that are difficult to verify
* fail to provide reliable source attribution
* mix factual information with unsupported interpretation

FinMitra aims to combine the strengths of both approaches.

```text
User Question
      │
      ▼
Query Understanding
      │
      ▼
Relevant Data Retrieval
      │
      ▼
Financial Tools / Agents
      │
      ▼
Evidence Verification
      │
      ▼
Deterministic Calculations
      │
      ▼
AI Explanation
      │
      ▼
Citations + Uncertainty
      │
      ▼
User
```

---

# Product Vision

FinMitra is being developed as an **evidence-first financial intelligence platform**, rather than an autonomous trading or investment-advisory system.

The long-term platform will provide three major capabilities:

```text
                    FinMitra
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Research       Portfolio      Education
    Intelligence    Analytics
        │              │              │
        └──────────────┼──────────────┘
                       │
                Evidence Engine
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Market Data       Filings        News
```

---

# Planned Features

## 🔎 Financial Research

Research companies and financial topics using structured data, retrieved evidence, and AI-generated explanations.

Example questions:

```text
Analyze Reliance Industries.

Compare TCS and Infosys.

What are the major risks for HDFC Bank?

Explain P/E ratio to a beginner.
```

---

## 📊 Portfolio Analytics

Users will be able to create portfolios and analyze:

* Portfolio value
* Investment amount
* Profit / loss
* Return percentage
* Asset allocation
* Sector exposure
* Concentration
* Historical performance
* Risk metrics

Financial calculations will be performed by deterministic application code rather than delegated to an LLM.

---

## 🤖 Agentic Financial Intelligence

FinMitra will use controlled agentic workflows rather than a single unrestricted AI agent.

Planned architecture:

```text
                    Supervisor
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
      Research       Portfolio     Education
       Agent           Agent         Agent
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                 Evidence Engine
                        │
                        ▼
                  Answer Agent
                        │
                        ▼
                  Safety Layer
```

---

## 📚 Evidence-First RAG

FinMitra will retrieve supporting evidence before generating financial explanations.

The planned retrieval pipeline is:

```text
Documents
    │
    ▼
Ingestion
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
PostgreSQL + pgvector
    │
    ├──────────────┐
    ▼              ▼
Keyword Search   Vector Search
    │              │
    └──────┬───────┘
           ▼
       Reranking
           │
           ▼
      Evidence Pack
           │
           ▼
      Answer Generation
```

Answers will eventually expose supporting sources, publication dates, retrieval dates, and relevant evidence.

---

## 🛡️ AI Safety

FinMitra is being designed with financial-domain safety as a core engineering requirement.

Planned controls include:

* Prompt-injection detection
* PII protection
* Tool permissions
* Rate limiting
* Output validation
* Citation validation
* Uncertainty handling
* Human approval for sensitive operations
* Audit logging

The system should prefer:

> "There is insufficient evidence to determine this."

over an unsupported financial claim.

---

# Technology Stack

## Frontend

* Next.js
* TypeScript
* Tailwind CSS
* shadcn/ui
* Recharts

## Backend

* Python 3.12+
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

## AI

* LangGraph
* LangChain
* MCP
* Provider-agnostic LLM abstraction
* Local and cloud LLM providers

Potential development providers include:

* Ollama
* Groq
* Google Gemini
* OpenRouter
* Other compatible providers

The architecture is intentionally provider-independent.

## Database

* PostgreSQL
* pgvector

PostgreSQL is intended to be the primary system of record for application and AI-related data.

## Infrastructure

Development:

* Docker
* Docker Compose

Planned production infrastructure:

* Containerized services
* Managed PostgreSQL
* Managed cache/queue infrastructure
* Cloud deployment
* GitHub Actions CI/CD

## Testing & Quality

* pytest
* pytest-asyncio
* HTTPX
* Ruff
* MyPy
* Locust
* GitHub Actions

---

# Architecture

The long-term architecture is planned around clear separation between AI reasoning, application logic, deterministic financial computation, and persistent data.

```text
                         ┌──────────────┐
                         │   Next.js    │
                         │   Frontend   │
                         └──────┬───────┘
                                │
                              HTTPS
                                │
                         ┌──────▼───────┐
                         │   FastAPI    │
                         │   Backend    │
                         └──────┬───────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
          API Layer        Application          MCP
                            Services
                                │
                         ┌──────▼───────┐
                         │  LangGraph   │
                         │    Runtime   │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
             Research       Portfolio      Education
               Agent          Agent          Agent
                 │              │              │
                 └──────────────┼──────────────┘
                                │
                         ┌──────▼───────┐
                         │ Tool Layer   │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
             Market Data      Search       Calculator
                                │
                         ┌──────▼───────┐
                         │   Evidence   │
                         │    Engine    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │ PostgreSQL   │
                         │  + pgvector  │
                         └──────────────┘
```

A key architectural principle is:

```text
LLM
 │
 │ interpretation / reasoning
 ▼
Application Services
 │
 │ controlled operations
 ▼
Deterministic Financial Engine
 │
 ▼
PostgreSQL
```

The LLM should not be responsible for:

* financial arithmetic
* portfolio accounting
* permission enforcement
* source validation
* database integrity
* financial-rule enforcement

---

# Repository Structure

```text
finmitra/
│
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── db/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   ├── agents/
│   │   │   ├── tools/
│   │   │   ├── retrieval/
│   │   │   ├── evaluation/
│   │   │   └── main.py
│   │   └── tests/
│   │
│   └── web/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── tests/
│
├── packages/
│   └── shared/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── evals/
│   ├── datasets/
│   └── results/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   └── research/
│
├── infra/
│   ├── docker/
│   └── deployment/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .env.example
├── Makefile
├── README.md
└── LICENSE
```

---

# Development Roadmap

FinMitra is being developed incrementally.

| Phase    | Milestone                         | Status     |
| -------- | --------------------------------- | ---------- |
| Phase 0  | Product & Engineering Foundation  | ✅ Complete |
| Phase 1  | Backend + PostgreSQL Foundation   | ✅ Complete |
| Phase 2  | Authentication                    | ✅ Complete |
| Phase 3  | Market Data Abstraction           | ✅ Complete |
| Phase 4  | Deterministic Portfolio Engine    | 🚀 Next    |
| Phase 5  | LLM Provider Abstraction          | ⚪ Planned  |
| Phase 6  | First Research Agent              | ⚪ Planned  |
| Phase 7  | LangGraph Workflows               | ⚪ Planned  |
| Phase 8  | RAG + Hybrid Retrieval            | ⚪ Planned  |
| Phase 9  | Evidence & Citations              | ⚪ Planned  |
| Phase 10 | Portfolio Agent                   | ⚪ Planned  |
| Phase 11 | Education Agent                   | ⚪ Planned  |
| Phase 12 | Safety Layer                      | ⚪ Planned  |
| Phase 13 | Alerts                            | ⚪ Planned  |
| Phase 14 | MCP Integration                   | ⚪ Planned  |
| Phase 15 | Evaluation Framework              | ⚪ Planned  |
| Phase 16 | Observability                     | ⚪ Planned  |
| Phase 17 | Performance & Caching             | ⚪ Planned  |
| Phase 18 | Frontend Product                  | ⚪ Planned  |
| Phase 19 | Security & Production Hardening   | ⚪ Planned  |
| Phase 20 | Cloud Deployment                  | ⚪ Planned  |
| Phase 21 | Public Beta                       | ⚪ Planned  |
| Phase 22 | Research / Evaluation Publication | ⚪ Planned  |

---

# Local Development

FinMitra is being developed **locally first**.

The initial development environment consists of:

```text
localhost

Next.js       :3000
     │
     ▼
FastAPI       :8000
     │
     ▼
PostgreSQL    :5432
     │
     ▼
pgvector
```

Docker Compose is used to make the development environment reproducible.

### Planned startup

```bash
docker compose up -d
```

The complete setup instructions are maintained in the [Phase 2 Setup Guide](docs/setup/phase-2-setup.md).

---

# Configuration

Environment-specific configuration is stored through environment variables.

A template is provided as:

```text
.env.example
```

Local secrets belong in:

```text
.env
```

`.env` must never be committed to the repository.

The application is designed so that local development and future cloud deployment use the same application architecture with different configuration.

---

# Development Philosophy

FinMitra follows several engineering principles.

### 1. Evidence before explanation

AI-generated financial claims should be grounded in retrieved evidence.

### 2. Deterministic calculations

Financial calculations should be performed by tested application code.

### 3. AI as an interpreter

LLMs should interpret and explain structured information rather than become the source of truth.

### 4. Provider independence

Changing the LLM provider should not require rewriting the agent architecture.

### 5. Evaluation-driven development

The system will eventually be evaluated using a dedicated financial question benchmark.

### 6. Safety by design

Financial-domain safety should be implemented as an architectural layer rather than a prompt-only instruction.

### 7. Reproducibility

The project should be runnable locally from a clean checkout with documented commands.

---

# Research Direction

FinMitra is also intended to serve as an experimental platform for research into reliable financial AI systems.

A potential research direction is:

> **Evidence-First Agentic Financial Intelligence: Improving Reliability and Safety of LLM-Based Financial Research Systems**

Possible experiments include comparing:

```text
Baseline LLM
      ↓
RAG
      ↓
Hybrid RAG
      ↓
Agentic RAG
      ↓
Agentic RAG + Evidence Verification
      ↓
Agentic RAG + Safety Guardrails
```

Potential evaluation metrics:

* Answer correctness
* Citation correctness
* Retrieval recall
* Retrieval precision
* MRR
* Tool-selection accuracy
* Faithfulness
* Hallucination rate
* Safety violation rate
* Latency
* Token usage
* Cost per query

---

# Open Source

FinMitra is being developed as an open-source project.

The goal is to make the architecture, implementation, evaluation methodology, and research findings transparent and reproducible.

Contributions, issues, discussions, and suggestions are welcome.

---

# Disclaimer

FinMitra is an educational and financial-information software project.

It is not intended to provide regulated investment advice, guarantee financial returns, execute autonomous trades, or replace a qualified financial professional.

Financial information can be incomplete, delayed, inaccurate, or subject to change. Users should independently verify important information and make their own financial decisions.

---

# Project Status

**Current Phase:** Phase 3 – Market Data Abstraction ✅

**Next Phase:** Phase 4 – Deterministic Portfolio Engine

The project is currently under active development.

---

# Author

**Koustubh Kulkarni**

Computer Science & Engineering

FinMitra is being developed as an open-source Applied AI, financial intelligence, and research project.

