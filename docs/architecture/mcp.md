# FinMitra Phase 6: MCP Architecture

## 1. Why MCP?
The Model Context Protocol (MCP) standardizes how AI agents interact with external tools and resources. 
By introducing MCP to FinMitra, we formally separate the LLM's reasoning engine from the underlying backend tool execution layer.

## 2. Server Architecture
- **Location**: `app/mcp_server.py`
- **Type**: Embedded local FastMCP server.
- **Purpose**: Exposes FinMitra's core financial capabilities (`get_portfolio_summary`, `get_stock_quote`, `get_user_portfolios`) as strictly typed MCP tools.

## 3. Tool Schemas
Every MCP tool defines strict Pydantic schemas. For example, `PortfolioSummaryInput` strictly expects a `portfolio_id` string, and validates its UUID formatting before querying the database.

## 4. MCP Authorization vs Application Authorization
- MCP does **NOT** replace application authorization.
- The `user_id` is never requested from the LLM. It is strictly injected securely into the tool closures at runtime, maintaining absolute user isolation.
- An MCP Client acting on behalf of User A physically cannot invoke a tool that accesses User B's portfolio, because the underlying service strictly requires the injected `user_uuid`.

## 5. Security & Limitations
- The embedded MCP server currently operates within the FastAPI process space. To scale horizontally, it can be decoupled into a standalone service utilizing SSE or Stdio transport, but for MVP it serves as a strict standard interface.
