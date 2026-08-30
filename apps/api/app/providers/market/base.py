from datetime import date
from typing import Protocol

from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)


class MarketDataProvider(Protocol):
    """Protocol defining the interface for all market data providers."""

    def get_quote(self, symbol: str) -> Quote:
        """Fetch the current quote for a given symbol."""
        ...

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        """Fetch historical prices for a given symbol over a specific date range and interval."""
        ...

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        """Fetch the company profile for a given symbol."""
        ...

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        """Fetch financial metrics for a given symbol."""
        ...
