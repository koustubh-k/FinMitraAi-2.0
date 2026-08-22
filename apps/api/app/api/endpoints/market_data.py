from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date, timedelta
from app.services.market_data import MarketDataService, get_market_data_service
from app.schemas.market_data import (
    Quote,
    HistoricalPriceResponse,
    CompanyProfile,
    FinancialMetrics,
    utc_now
)
from app.core.errors import (
    SymbolNotFoundError,
    ProviderUnavailableError,
    RateLimitError,
    InvalidMarketDataError
)

router = APIRouter()

def handle_market_error(e: Exception):
    if isinstance(e, SymbolNotFoundError):
        raise HTTPException(status_code=404, detail=str(e))
    elif isinstance(e, RateLimitError):
        raise HTTPException(status_code=429, detail="Market data provider rate limit exceeded")
    elif isinstance(e, ProviderUnavailableError):
        raise HTTPException(status_code=503, detail="Market data provider unavailable")
    elif isinstance(e, InvalidMarketDataError):
        raise HTTPException(status_code=502, detail="Invalid data received from market provider")
    else:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching market data")

@router.get("/quote/{symbol}", response_model=Quote)
def get_quote(
    symbol: str,
    market_service: MarketDataService = Depends(get_market_data_service)
):
    try:
        return market_service.get_quote(symbol)
    except Exception as e:
        handle_market_error(e)

@router.get("/history/{symbol}", response_model=HistoricalPriceResponse)
def get_history(
    symbol: str,
    start: date = Query(None, description="Start date (defaults to 30 days ago)"),
    end: date = Query(None, description="End date (defaults to today)"),
    interval: str = Query("1d", description="Data interval (e.g., 1d, 1wk, 1mo)"),
    market_service: MarketDataService = Depends(get_market_data_service)
):
    if not end:
        end = utc_now().date()
    if not start:
        start = end - timedelta(days=30)
        
    if start > end:
        raise HTTPException(status_code=422, detail="Start date cannot be after end date")

    try:
        return market_service.get_historical_prices(symbol, start, end, interval)
    except Exception as e:
        handle_market_error(e)

@router.get("/company/{symbol}", response_model=CompanyProfile)
def get_company_profile(
    symbol: str,
    market_service: MarketDataService = Depends(get_market_data_service)
):
    try:
        return market_service.get_company_profile(symbol)
    except Exception as e:
        handle_market_error(e)

@router.get("/metrics/{symbol}", response_model=FinancialMetrics)
def get_financial_metrics(
    symbol: str,
    market_service: MarketDataService = Depends(get_market_data_service)
):
    try:
        return market_service.get_financial_metrics(symbol)
    except Exception as e:
        handle_market_error(e)
