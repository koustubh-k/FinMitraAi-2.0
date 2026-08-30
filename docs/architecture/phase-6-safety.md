# FinMitra Phase 6: Safety Architecture

## 1. Trust Boundaries
- **Trusted**: Backend Application Code, Validated Tool Results, Financial Engine (Decimal calculations).
- **Untrusted**: User Queries, Uploaded Documents, Retrieved RAG Context, LLM Outputs.

## 2. Prompt Injection Defenses
- The system prevents the LLM from executing malicious instructions hidden in retrieved documents or user queries.
- **Implementation**: The `ResearchAgent` wraps retrieved evidence in `<context>` blocks. The System Prompt explicitly instructs the LLM to treat everything inside the `<context>` block as untrusted data, specifically forbidding the execution of any embedded commands.
- **Supervisor Defense**: The Supervisor is instructed to ignore user attempts to override the routing logic.

## 3. Tool Permissions & Authorization
- Tools like `get_portfolio_summary` are **bound** to the authenticated user's `user_id` inside the backend.
- The LLM cannot provide a arbitrary `user_id` (e.g. cross-user access).
- Tool schemas (via Pydantic) validate inputs like `portfolio_id` before execution.

## 4. Execution Limits
- **Timeouts**: Expensive or external tools (like `get_stock_quote` or portfolio database queries) use `asyncio.wait_for` with hard timeouts (e.g., 5-10 seconds) to prevent the agent workflow from hanging indefinitely.
- **Agent Loops**: The LangGraph engine is compiled with `recursion_limit=10` to prevent runaway reasoning loops. Internally, the PortfolioAgent restricts tool-calling iteration to 5 steps.

## 5. Secret Protection
- Errors from tools are caught and converted into user-friendly messages (e.g., "Unable to retrieve portfolios") rather than leaking stack traces, SQL syntax, or internal filesystem paths.
