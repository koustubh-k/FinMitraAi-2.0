# Multi-Agent System Architecture (Phase 5)

FinMitra 2.0 uses a Supervisor-based Multi-Agent Orchestration model powered by LangGraph. This allows specialized agents to handle distinct domains while providing a unified conversational interface to the user.

## Supervisor Agent
The Supervisor is the entry point for all queries. It uses a strictly typed LLM output schema to classify the user's request into one of four routes:
- `portfolio`: Requires looking up the user's personal financial data or analyzing their holdings.
- `research`: Requires retrieving current market news, external documents, or company fundamentals via the RAG pipeline.
- `education`: Requires explaining financial concepts, terminology, or formulas.
- `general`: Simple fallback for greetings and conversational pleasantries.

## Agents
1. **Portfolio Agent:** Equipped with deterministic tools that access the `PortfolioService`. It is strictly forbidden from performing its own financial arithmetic.
2. **Education Agent:** A zero-tool agent equipped with a specialized prompt to explain financial concepts at varying levels of complexity (beginner, intermediate, advanced) without providing personalized financial advice.
3. **Research Agent:** The existing Phase 4 Evidence-First RAG pipeline, repurposed as a subgraph/node that is invoked by the Supervisor.

## State Management (`AssistantState`)
The system passes an `AssistantState` object through the graph. Key fields include:
- `user_id`: Injected securely at the API boundary; used to bind database tools to the authenticated user.
- `route`: The decision made by the Supervisor.
- `status`: Streamed to the frontend to communicate progress without exposing chain-of-thought (e.g., `analyzing_portfolio`).

## Handoffs and Loop Prevention
Currently, the graph routes linearly: `Supervisor → Specialized Agent → END`. 
If a specialized agent requires capabilities from another (e.g., Portfolio Agent needing Research), future phases will support explicit bounded handoffs (max steps = 5) to prevent infinite loops.
