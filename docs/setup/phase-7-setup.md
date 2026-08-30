# Phase 7 Setup & Observability Guide

## 1. Environment Variables
To enable LangSmith tracing and structured logging, ensure your `.env` file at the root of the project includes:

```bash
# LangSmith Observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<your-langsmith-api-key>
LANGCHAIN_PROJECT=finmitra-2.0
```

> [!WARNING]
> Without a valid `LANGCHAIN_API_KEY`, the application will continue to function, but it will print 401 Unauthorized errors in the background when attempting to upload traces.

## 2. Structured Logging
Logs across the FastAPI backend are now written in JSON format containing a `request_id`.
When viewing logs in Kubernetes, Docker, or Google Cloud Logging, you can filter by `request_id` to trace an individual user query across all agents and tools.

## 3. Running Automated Evals
To run the evaluation suite locally:
```bash
cd apps/api
# Ensure your PYTHONPATH is set so python can resolve the app module
$env:PYTHONPATH="." (Windows) / export PYTHONPATH="." (Mac/Linux)
python evals/runners/run_evals.py
```
