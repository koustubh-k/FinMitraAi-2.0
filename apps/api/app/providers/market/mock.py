from datetime import date, datetime, timezone, timedelta
from app.schemas.market_data import (
    Quote,
    HistoricalPrice,
    HistoricalPriceResponse,
    CompanyProfile,
    FinancialMetrics,
    utc_now
)
from app.core.errors import SymbolNotFoundError
from app.providers.market.base import MarketDataProvider

class MockMarketDataProvider:
    """A deterministic mock market data provider for testing."""

    def get_quote(self, symbol: str) -> Quote:
        if "INVALID" in symbol:
            raise SymbolNotFoundError(symbol)
        
        return Quote(
            symbol=symbol,
            price=100.0,
            currency="INR",
            timestamp=utc_now(),
            previous_close=98.5,
            day_change=1.5,
            day_change_percent=1.52,
            data_timestamp=utc_now()
        )

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        if "INVALID" in symbol:
            raise SymbolNotFoundError(symbol)

        # Generate some mock data between start and end
        data = []
        current = datetime.combine(start, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(end, datetime.min.time()).replace(tzinfo=timezone.utc)
        
        price = 100.0
        while current <= end_dt:
            data.append(
                HistoricalPrice(
                    timestamp=current,
                    open=price,
                    high=price + 2.0,
                    low=price - 1.0,
                    close=price + 1.0,
                    adjusted_close=price + 1.0,
                    volume=10000
                )
            )
            price += 1.0
            current += timedelta(days=1)
            
        return HistoricalPriceResponse(
            symbol=symbol,
            interval=interval,
            data=data
        )

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        if "INVALID" in symbol:
            raise SymbolNotFoundError(symbol)
            
        return CompanyProfile(
            symbol=symbol,
            name=f"{symbol} Corporation",
            exchange="NSE",
            currency="INR",
            sector="Technology",
            industry="Software",
            country="India",
            data_timestamp=utc_now()
        )

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        if "INVALID" in symbol:
            raise SymbolNotFoundError(symbol)
            
        return FinancialMetrics(
            symbol=symbol,
            market_cap=1000000000.0,
            pe_ratio=25.5,
            eps=4.0,
            dividend_yield=1.2,
            beta=1.1,
            data_timestamp=utc_now()
        )
