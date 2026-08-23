import pytest
from datetime import date, timedelta
from app.providers.market.registry import provider_registry
from app.schemas.market_data import (
    Quote,
    HistoricalPriceResponse,
    CompanyProfile,
    FinancialMetrics
)
from app.core.errors import SymbolNotFoundError

# Test against both providers to ensure they honor the same contract
# If testing locally without internet, the yahoo tests might fail/timeout.
# To handle this, we could mark yahoo tests with @pytest.mark.network,
# but for now we'll run them to ensure the contract works.

@pytest.fixture(params=["mock", "yahoo"])
def provider(request):
    return provider_registry.get(request.param)

@pytest.fixture
def test_symbol(request):
    # Use Reliance as a known symbol for both providers
    # The mock provider accepts any symbol, but yahoo needs the actual symbol
    return "RELIANCE.NS" 

def test_get_quote_contract(provider, test_symbol):
    quote = provider.get_quote(test_symbol)
    assert isinstance(quote, Quote)
    assert quote.symbol == test_symbol
    assert isinstance(quote.price, float)
    assert isinstance(quote.currency, str)

def test_get_historical_prices_contract(provider, test_symbol):
    end = date.today()
    start = end - timedelta(days=5)
    
    history = provider.get_historical_prices(test_symbol, start, end, "1d")
    assert isinstance(history, HistoricalPriceResponse)
    assert history.symbol == test_symbol
    assert isinstance(history.data, list)
    
    if len(history.data) > 0:
        first_point = history.data[0]
        assert hasattr(first_point, "close")
        assert hasattr(first_point, "volume")

def test_get_company_profile_contract(provider, test_symbol):
    profile = provider.get_company_profile(test_symbol)
    assert isinstance(profile, CompanyProfile)
    assert profile.symbol == test_symbol
    assert profile.name is not None

def test_get_financial_metrics_contract(provider, test_symbol):
    metrics = provider.get_financial_metrics(test_symbol)
    assert isinstance(metrics, FinancialMetrics)
    assert metrics.symbol == test_symbol

def test_invalid_symbol_contract(provider):
    with pytest.raises(SymbolNotFoundError):
        provider.get_quote("INVALID_SYMBOL_THAT_DOES_NOT_EXIST.NS")
