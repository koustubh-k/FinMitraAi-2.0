# FinMitra 2.0 - Phase 4 Setup Guide

This guide explains how to set up the Phase 4 AI Research MVP, specifically focusing on the new free LLM providers, Market Data providers, and the pgvector database.

## 1. Database (pgvector)
Phase 4 relies on Postgres `pgvector` for semantic document search.
If you are running the project via Docker, the `docker-compose.yml` automatically uses the `pgvector/pgvector:pg16` image.

```bash
docker compose up -d postgres
```

## 2. Setting up LLM Providers

FinMitra 2.0 uses a "Provider Independence" model. You can configure which LLM to use by setting the `LLM_PROVIDER` in your `.env` file. We recommend using free providers to keep development costs low.

### Recommended Providers:

#### A. GroqCloud (Best for Speed/Agents)
Groq uses LPUs for incredibly fast inference, which is ideal for LangGraph agentic workflows.
1. Sign up at [console.groq.com](https://console.groq.com/).
2. Navigate to "API Keys" and generate a key.
3. Update your `.env`:
   ```env
   LLM_PROVIDER=groq
   LLM_MODEL=llama3-8b-8192
   GROQ_API_KEY=gsk_...
   ```

#### B. Google AI Studio (Best for Massive Documents)
Gemini 1.5 Flash has a huge context window, perfect for stuffing large 10-K filings.
1. Sign up at [aistudio.google.com](https://aistudio.google.com/).
2. Click "Get API Key" on the left sidebar.
3. Update your `.env`:
   ```env
   LLM_PROVIDER=gemini
   LLM_MODEL=gemini-1.5-flash
   GEMINI_API_KEY=AIzaSy...
   ```

#### C. OpenRouter (Best for Provider Routing)
OpenRouter provides a unified OpenAI-compatible endpoint that routes to dozens of free models.
1. Sign up at [openrouter.ai](https://openrouter.ai/).
2. Go to Settings > API Keys and create a key.
3. Update your `.env`:
   ```env
   LLM_PROVIDER=openrouter
   LLM_MODEL=mistralai/mistral-7b-instruct:free
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

## 3. Market Data Providers

FinMitra uses a registry pattern to allow switching between market data providers.

### Available Providers:
1. **AlphaVantage**: Get a free API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key).
2. **Finnhub**: Get a free API key at [finnhub.io](https://finnhub.io/register).
3. **FMP (Financial Modeling Prep)**: Get a free API key at [site.financialmodelingprep.com](https://site.financialmodelingprep.com/developer/docs).

Set your preferred provider in `.env`:
```env
MARKET_DATA_PROVIDER=alphavantage
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
```

## 4. Running the Agent

With your keys set, you can run the FastAPI backend and navigate to the frontend Research Dashboard.

```bash
docker compose up -d api web
```

Navigate to `http://localhost:3000/research` to access the streaming agent UI.
