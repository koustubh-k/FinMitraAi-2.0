from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List
from uuid import UUID
from pydantic import Field
from contextlib import contextmanager

from app.db.session import SessionLocal
from app.services.portfolio import PortfolioService
from app.providers.market.registry import ProviderRegistry

# Create the FastMCP server
mcp = FastMCP("FinMitra")


@contextmanager
def get_db():
    """Context manager that guarantees the session is always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_market_data_service():
    from app.services.market_data import MarketDataService
    registry = ProviderRegistry()
    return MarketDataService(registry)

@mcp.tool()
def get_portfolio_summary(user_id: str = Field(description="The authenticated user UUID"), portfolio_id: str = Field(description="The UUID of the portfolio to summarize")) -> str:
    """Get a detailed summary of a specific portfolio including holdings, PnL, cost basis, and market value."""
    with get_db() as db:
        try:
            service = PortfolioService(db)
            market_service = get_market_data_service()
            summary = service.get_portfolio_summary(UUID(user_id), UUID(portfolio_id), market_service)
            return summary.model_dump_json()
        except Exception as e:
            return f"Error: {str(e)}"

@mcp.tool()
def get_user_portfolios(user_id: str = Field(description="The authenticated user UUID")) -> str:
    """Get a list of all portfolios owned by the user, including their IDs and names."""
    with get_db() as db:
        try:
            service = PortfolioService(db)
            portfolios = service.get_user_portfolios(UUID(user_id))
            return str([{"id": str(p.id), "name": p.name} for p in portfolios])
        except Exception as e:
            return f"Error: {str(e)}"

@mcp.tool()
def get_stock_quote(symbol: str = Field(description="The stock ticker symbol")) -> str:
    """Get the current market price and quote data for a given stock ticker symbol."""
    try:
        market_service = get_market_data_service()
        quote = market_service.get_quote(symbol)
        if quote:
            return quote.model_dump_json()
        return f"Error: Could not retrieve quote for {symbol}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
