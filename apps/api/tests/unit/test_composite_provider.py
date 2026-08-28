import pytest
from datetime import date
from decimal import Decimal

from app.core.errors import ProviderUnavailableError, SymbolNotFoundError
from app.providers.market.composite import CompositeMarketDataProvider
from app.providers.market.duckduckgo import DuckDuckGoProvider
from app.schemas.market_data import Quote


class MockFailingProvider:
    def get_quote(self, symbol: str):
        raise ProviderUnavailableError("Failing provider")

    def get_historical_prices(self, symbol, start, end, interval):
        raise ProviderUnavailableError("Failing provider")

    def get_company_profile(self, symbol):
        raise ProviderUnavailableError("Failing provider")

    def get_financial_metrics(self, symbol):
        raise ProviderUnavailableError("Failing provider")


from datetime import datetime, timezone

class MockSucceedingProvider:
    def get_quote(self, symbol: str):
        if symbol == "INVALID":
            raise SymbolNotFoundError(symbol)
        now = datetime.now(timezone.utc)
        return Quote(
            symbol=symbol, 
            price=150.0, 
            currency="USD", 
            source="mock",
            timestamp=now,
            data_timestamp=now
        )


def test_composite_provider_success():
    """Test that the composite provider successfully falls back to the succeeding provider."""
    failing = MockFailingProvider()
    succeeding = MockSucceedingProvider()
    
    composite = CompositeMarketDataProvider([failing, succeeding])
    quote = composite.get_quote("AAPL")
    
    assert quote.symbol == "AAPL"
    assert quote.price == 150.0


def test_composite_provider_all_fail():
    """Test that it raises ProviderUnavailableError if all fail."""
    failing1 = MockFailingProvider()
    failing2 = MockFailingProvider()
    
    composite = CompositeMarketDataProvider([failing1, failing2])
    
    with pytest.raises(ProviderUnavailableError):
        composite.get_quote("AAPL")


def test_composite_provider_symbol_not_found():
    """Test that it propagates SymbolNotFoundError immediately without falling back."""
    succeeding = MockSucceedingProvider()
    # succeeding raises SymbolNotFoundError for "INVALID"
    # Even if there was another provider after it, it should raise immediately
    failing = MockFailingProvider()
    
    composite = CompositeMarketDataProvider([succeeding, failing])
    
    with pytest.raises(SymbolNotFoundError):
        composite.get_quote("INVALID")


def test_duckduckgo_extract_price():
    """Test the regex extraction logic in DuckDuckGoProvider."""
    provider = DuckDuckGoProvider()
    
    assert provider._extract_price("AAPL stock price is 150.25 USD") == Decimal("150.25")
    assert provider._extract_price("Price: $1,234.56 today") == Decimal("1234.56")
    assert provider._extract_price("Currently trading at ₹ 3500.00") == Decimal("3500.00")
    assert provider._extract_price("Just 100") == Decimal("100")
    assert provider._extract_price("No price here") is None

