# Deterministic Financial Engine Architecture

## Overview

The FinMitra 2.0 Deterministic Financial Engine provides a pure, stateless mathematical core for all portfolio calculations. It calculates average cost, P&L (Realized and Unrealized), and portfolio allocations. 

## Key Principles

1. **Source of Truth**: The `financial.engine` module is the sole source of truth for portfolio metrics.
2. **Deterministic & Pure**: All functions in `engine.py` are pure functions. They take explicit numerical inputs and return explicit numerical outputs. They have *no* dependencies on SQLAlchemy, FastAPI, or external network calls.
3. **Immutability & Precision**: All calculations use Python's `decimal.Decimal` to avoid floating-point errors.
4. **No LLM Math**: Generative AI components are explicitly forbidden from calculating portfolio values or returns. They must rely on the APIs powered by this engine.

## Core Operations

### 1. Cost Basis & Average Cost

The average cost of a position is updated on every `BUY` transaction using a weighted average formula:
```
new_average_cost = ((current_qty * current_avg_cost) + (buy_qty * buy_price)) / (current_qty + buy_qty)
```

The cost basis for a holding is calculated as:
```
cost_basis = holding_quantity * average_cost
```

### 2. Realized & Unrealized P&L

- **Realized P&L** is calculated at the time of a `SELL` transaction:
  ```
  realized_pnl = (sell_qty * sell_price) - (sell_qty * average_cost)
  ```
  *Note: To calculate portfolio-level historical realized P&L, the engine processes all historical transactions to accurately track the moving average cost at the time of each sale.*

- **Unrealized P&L** is calculated dynamically based on current market prices:
  ```
  unrealized_pnl = market_value - cost_basis
  ```

- **Total P&L** is the sum of both:
  ```
  total_pnl = realized_pnl + unrealized_pnl
  ```

### 3. Allocation & Returns

- **Allocation**: The weight of a single position relative to the entire portfolio.
  ```
  allocation_percentage = (position_market_value / portfolio_market_value) * 100
  ```

- **Return Percentage**: The simple return of the portfolio relative to invested capital.
  ```
  return_percentage = (total_pnl / portfolio_cost_basis) * 100
  ```

## Integration with Services

The `PortfolioService` orchestrates data retrieval and integrates with the engine:
1. Fetches current holdings and transaction history from the database.
2. Retrieves current market quotes via `MarketDataService`.
3. Passes numerical inputs (`Decimal`) to the engine's pure functions.
4. Aggregates results into `PortfolioSummary` and `AllocationResponse` schemas for the API layer.

### Market Data Fallback Strategy

To ensure deterministic reporting even when external APIs fail, the `MarketDataService` employs a **Composite Provider Architecture**. 
- It accepts a prioritized, comma-separated list of providers (e.g., `yahoo,duckduckgo`).
- **Primary APIs** (e.g., `YahooProvider`) are queried first for structured, accurate data.
- **Fallback Web Search** (e.g., `DuckDuckGoProvider`) is queried if the primary API raises a `ProviderUnavailableError`. The DuckDuckGo provider uses regex heuristics on unstructured search snippets to extract basic current stock prices.
- If a stock ticker is truly invalid, providers raise a `SymbolNotFoundError`, halting the fallback chain immediately to prevent slow timeouts.

### Concurrency

When processing transactions, `PortfolioService` uses database row-level locking (`SELECT ... FOR UPDATE`) during the nested transaction (`db.begin_nested()`) to prevent race conditions when updating a holding's quantity and average cost concurrently.
