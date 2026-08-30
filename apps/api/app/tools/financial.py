import asyncio
from typing import Optional, Dict, Any, List
from langchain_core.tools import StructuredTool
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.portfolio import PortfolioService
from app.providers.market.registry import ProviderRegistry
from uuid import UUID
from pydantic import BaseModel, Field
from contextlib import contextmanager


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

class PortfolioSummaryInput(BaseModel):
    portfolio_id: str = Field(description="The UUID of the portfolio to summarize.")

class StockQuoteInput(BaseModel):
    symbol: str = Field(description="The stock ticker symbol (e.g. AAPL, TCS).")

async def _get_portfolio_summary_safe(user_uuid: UUID, portfolio_id: str) -> str:
    """Safe wrapper with timeout and validation for getting portfolio summary."""
    try:
        pid = UUID(portfolio_id)
    except ValueError:
        return '{"error": "Invalid portfolio_id format. Must be a valid UUID."}'

    try:
        def fetch():
            with get_db() as db:
                service = PortfolioService(db)
                market_service = get_market_data_service()
                return service.get_portfolio_summary(user_uuid, pid, market_service).model_dump_json()
            
        result = await asyncio.wait_for(asyncio.to_thread(fetch), timeout=10.0)
        return result
    except asyncio.TimeoutError:
        return '{"error": "Portfolio summary request timed out. Please try again later."}'
    except Exception:
        # Hide internal stack traces, log securely in a real app
        return '{"error": "Unable to retrieve portfolio summary. Verify you own this portfolio."}'

async def _get_user_portfolios_safe(user_uuid: UUID) -> str:
    """Safe wrapper with timeout for listing user portfolios."""
    try:
        def fetch():
            with get_db() as db:
                service = PortfolioService(db)
                portfolios = service.get_user_portfolios(user_uuid)
                import json
                return json.dumps([{"id": str(p.id), "name": p.name} for p in portfolios])
            
        result = await asyncio.wait_for(asyncio.to_thread(fetch), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        return '{"error": "Request timed out."}'
    except Exception:
        return '{"error": "Unable to retrieve portfolios."}'

async def _get_stock_quote_safe(symbol: str) -> str:
    """Safe wrapper with timeout for fetching market quotes."""
    if not symbol.isalnum() or len(symbol) > 10:
        return '{"error": "Invalid symbol."}'
        
    try:
        def fetch():
            market_service = get_market_data_service()
            quote = market_service.get_quote(symbol)
            if quote:
                return quote.model_dump_json()
            return '{"error": "Could not retrieve quote."}'
            
        result = await asyncio.wait_for(asyncio.to_thread(fetch), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        return '{"error": "Market data provider timed out."}'
    except Exception:
        return '{"error": "Unable to retrieve market quote."}'

def get_portfolio_tools(user_id: str) -> List[StructuredTool]:
    """Returns tools bound securely to the authenticated user's ID."""
    user_uuid = UUID(user_id)
    
    summary_tool = StructuredTool.from_function(
        coroutine=lambda portfolio_id: _get_portfolio_summary_safe(user_uuid, portfolio_id),
        name="get_portfolio_summary",
        description="Get a detailed summary of a specific portfolio including holdings, PnL, cost basis, and market value.",
        args_schema=PortfolioSummaryInput
    )
    
    list_tool = StructuredTool.from_function(
        coroutine=lambda: _get_user_portfolios_safe(user_uuid),
        name="get_user_portfolios",
        description="Get a list of all portfolios owned by the user, including their IDs and names. Call this to find the portfolio_id."
    )
    
    quote_tool = StructuredTool.from_function(
        coroutine=_get_stock_quote_safe,
        name="get_stock_quote",
        description="Get the current market price and quote data for a given stock ticker symbol.",
        args_schema=StockQuoteInput
    )
    
    return [summary_tool, list_tool, quote_tool]
