# Observability Architecture

## 1. Tracing via LangSmith
LangSmith is deeply integrated into the FinMitra architecture to capture all LLM inputs, outputs, tokens, and tool invocations.

- **Tracing Propagation**: The `LANGCHAIN_TRACING_V2=true` environment variable automatically injects tracing into all LangChain Runnables.
- **Agent Tags**: Explicit tags (e.g. `agent:research`, `agent:portfolio`, `agent:supervisor`) are injected into the `.invoke()` calls. This allows filtering traces in the LangSmith dashboard to diagnose performance bottlenecks or reasoning failures within specific agents.
- **User Association**: We inject `user:{user_id}` as a tag to map traces to specific user sessions.

## 2. Structured JSON Logging
FinMitra replaces the default Python logger with a structured JSON formatter (`app.core.logger`).

- **Format**: All logs are emitted as JSON objects, making them compatible with modern log aggregators (ELK, Datadog, GCP Logging).
- **Request ID Tracking**: A `RequestIDMiddleware` generates an `X-Request-ID` for every HTTP request and sets it in a `contextvars` variable. The logger pulls this variable and injects it into every log line spawned by that request, allowing complete end-to-end correlation across all synchronous and asynchronous tasks triggered by that request.

## 3. Metrics (TTFT & Latency)
The `RequestIDMiddleware` automatically captures total execution time (`duration_ms`) and logs it at the completion of every request. Future iterations will expose these metrics via a Prometheus `/metrics` endpoint if required by infrastructure.
