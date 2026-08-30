# Phase 5 Setup Guide: Multi-Agent Assistant

This guide explains how to set up and test the Multi-Agent Assistant (Phase 5) locally.

## Prerequisites
Ensure you have completed the Phase 4 setup, specifically configuring your `.env` file with LLM Providers (e.g. `GROQ_API_KEY` or `GEMINI_API_KEY`) and Market Data Providers.

## 1. Authentication Configuration
Unlike Phase 4, the unified Assistant API requires authentication because the Portfolio Agent needs to look up your personal investments.

Ensure you have a user account created in the database. You can do this by sending a `POST` request to `http://localhost:8000/auth/register` with a username and password.

## 2. API Usage (Backend)
To query the assistant via the backend directly:

1. Obtain a JWT token:
   ```bash
   curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"username": "youruser", "password": "yourpassword"}'
   ```
2. Send a query to the Assistant streaming endpoint:
   ```bash
   curl -N -X POST "http://localhost:8000/assistant/chat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_TOKEN_HERE" \
        -d '{"query": "What is the P/E ratio?"}'
   ```

## 3. Frontend Usage
Navigate to `http://localhost:3000/assistant`.
The UI now automatically streams status events like "Analyzing your portfolio..." or "Preparing explanation..." depending on which agent the Supervisor routes your query to.

*Note: You must be logged into the web application so the browser can attach the Authorization header.*

## 4. Manual Verification Scenarios
Try the following queries to verify the Supervisor routing works:
- **"Explain beta to me"** -> Routes to `Education Agent`.
- **"What is my portfolio worth?"** -> Routes to `Portfolio Agent` (will retrieve live market data and your DB holdings).
- **"What are the risks facing TCS?"** -> Routes to `Research Agent` (triggers RAG pipeline).
- **"Hello!"** -> Routes to `General Agent`.
