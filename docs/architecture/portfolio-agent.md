# Portfolio Agent Architecture

The Portfolio Agent is designed to securely analyze a user's holdings and performance.

## Tool-Driven Determinism
The Portfolio Agent MUST use tools to retrieve numbers. It is explicitly instructed not to perform its own calculations (e.g. subtracting cost basis from market value to find unrealized P&L).

### Available Tools
1. `get_user_portfolios()`: Lists the names and UUIDs of portfolios owned by the authenticated user.
2. `get_portfolio_summary(portfolio_id)`: Returns a structured JSON payload containing positions, market values, and P&L.
3. `get_stock_quote(symbol)`: Fetches live/delayed pricing via the MarketDataRegistry.

## Security Boundary
Tools are instantiated dynamically per request in `app/tools/financial.py`. The authenticated `user_id` is injected directly into the tool functions via Python closures (`functools.partial` or lambdas) rather than being accepted as a parameter from the LLM. 
This prevents Prompt Injection attacks where the LLM might attempt to request data for `user_id = 123`.

## UI Integration
When the Portfolio Agent returns its textual explanation, the raw tool results (e.g., the JSON from `get_portfolio_summary`) are also passed back through `AssistantState.tool_results`. The frontend UI can intercept these to render beautiful visual cards (e.g., "Total P&L: +$1,200") alongside the agent's textual summary.
