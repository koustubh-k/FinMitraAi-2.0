from typing import Optional, Dict, Any, List
from langchain_core.tools import StructuredTool
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.portfolio import PortfolioService
from app.providers.market.registry import MarketDataRegistry
from uuid import UUID

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_market_data_service():
    from app.services.market_data import MarketDataService
    registry = MarketDataRegistry()
    return MarketDataService(registry)

def _get_portfolio_summary(user_id: UUID, portfolio_id: str) -> Dict[str, Any]:
    """Get a detailed summary of a specific portfolio including holdings, PnL, cost basis, and market value."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        service = PortfolioService(db)
        market_service = get_market_data_service()
        summary = service.get_portfolio_summary(user_id, UUID(portfolio_id), market_service)
        return summary.model_dump()
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

def _get_user_portfolios(user_id: UUID) -> List[Dict[str, Any]]:
    """Get a list of all portfolios owned by the user, including their IDs and names."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        service = PortfolioService(db)
        portfolios = service.get_user_portfolios(user_id)
        return [{"id": str(p.id), "name": p.name} for p in portfolios]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        db.close()

def _get_stock_quote(symbol: str) -> Dict[str, Any]:
    """Get the current market price and quote data for a given stock ticker symbol."""
    try:
        market_service = get_market_data_service()
        quote = market_service.get_quote(symbol)
        if quote:
            return quote.model_dump()
        return {"error": f"Could not retrieve quote for {symbol}"}
    except Exception as e:
        return {"error": str(e)}

def get_portfolio_tools(user_id: str) -> List[StructuredTool]:
    """Returns tools bound securely to the authenticated user's ID."""
    user_uuid = UUID(user_id)
    
    summary_tool = StructuredTool.from_function(
        func=lambda portfolio_id: _get_portfolio_summary(user_uuid, portfolio_id),
        name="get_portfolio_summary",
        description="Get a detailed summary of a specific portfolio including holdings, PnL, cost basis, and market value. Requires portfolio_id."
    )
    
    list_tool = StructuredTool.from_function(
        func=lambda: _get_user_portfolios(user_uuid),
        name="get_user_portfolios",
        description="Get a list of all portfolios owned by the user, including their IDs and names. Call this to find the portfolio_id."
    )
    
    quote_tool = StructuredTool.from_function(
        func=_get_stock_quote,
        name="get_stock_quote",
        description="Get the current market price and quote data for a given stock ticker symbol."
    )
    
    return [summary_tool, list_tool, quote_tool]
