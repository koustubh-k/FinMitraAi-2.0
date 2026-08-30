from datetime import date

import pytest

from app.core.errors import SymbolNotFoundError
from app.services.market_data import MarketDataService


def test_market_data_service_initialization():
    service = MarketDataService(provider_name="mock")
    assert service.provider_name == "mock"

def test_normalize_symbol():
    service = MarketDataService(provider_name="yahoo")
    
    # Should append .NS if dot is not present and provider is yahoo
    assert service.normalize_symbol("RELIANCE") == "RELIANCE.NS"
    assert service.normalize_symbol(" reliance ") == "RELIANCE.NS"
    assert service.normalize_symbol("TCS.NS") == "TCS.NS"
    assert service.normalize_symbol("AAPL.O") == "AAPL.O"

def test_normalize_symbol_mock():
    service = MarketDataService(provider_name="mock")
    assert service.normalize_symbol("RELIANCE") == "RELIANCE"

def test_get_quote_success():
    service = MarketDataService(provider_name="mock")
    quote = service.get_quote("RELIANCE")
    
    assert quote.symbol == "RELIANCE"
    assert quote.price == 100.0
    assert quote.currency == "INR"

def test_get_quote_invalid_symbol():
    service = MarketDataService(provider_name="mock")
    with pytest.raises(SymbolNotFoundError):
        service.get_quote("INVALID")

def test_get_historical_prices():
    service = MarketDataService(provider_name="mock")
    start = date(2026, 1, 1)
    end = date(2026, 1, 5)
    
    history = service.get_historical_prices("RELIANCE", start, end, "1d")
    
    assert history.symbol == "RELIANCE"
    assert len(history.data) == 5
    assert history.data[0].open == 100.0

def test_get_company_profile():
    service = MarketDataService(provider_name="mock")
    profile = service.get_company_profile("TCS")
    
    assert profile.symbol == "TCS"
    assert profile.name == "TCS Corporation"

def test_get_financial_metrics():
    service = MarketDataService(provider_name="mock")
    metrics = service.get_financial_metrics("INFY")
    
    assert metrics.symbol == "INFY"
    assert metrics.pe_ratio == 25.5
