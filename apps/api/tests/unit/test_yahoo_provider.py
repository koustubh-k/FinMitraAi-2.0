from datetime import date, datetime, timezone
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.core.errors import (
    InvalidMarketDataError,
    ProviderUnavailableError,
    SymbolNotFoundError,
)
from app.providers.market.yahoo import YahooProvider


@pytest.fixture
def provider():
    return YahooProvider()

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_quote_success(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.fast_info.last_price = 100.0
    mock_ticker.fast_info.previous_close = 95.0
    mock_ticker.fast_info.currency = 'USD'
    mock_ticker_class.return_value = mock_ticker
    
    quote = provider.get_quote("AAPL")
    assert quote.symbol == "AAPL"
    assert quote.price == 100.0
    assert quote.previous_close == 95.0
    assert quote.day_change == 5.0
    assert round(quote.day_change_percent, 2) == 5.26

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_quote_missing_price(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.fast_info.last_price = None
    mock_ticker_class.return_value = mock_ticker
    
    with pytest.raises(SymbolNotFoundError):
        provider.get_quote("INVALID")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_quote_exception(mock_ticker_class, provider):
    # Simulate yfinance exception (AttributeError is common for no fast_info)
    mock_ticker_class.side_effect = Exception("Some connection error")
    
    with pytest.raises(InvalidMarketDataError):
        provider.get_quote("AAPL")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_quote_rate_limit(mock_ticker_class, provider):
    mock_ticker_class.side_effect = Exception("Rate limit exceeded")
    
    with pytest.raises(ProviderUnavailableError):
        provider.get_quote("AAPL")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_historical_prices_success(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    
    # Create sample DataFrame
    dates = [datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc)]
    df = pd.DataFrame({
        'Open': [100, 101],
        'High': [102, 103],
        'Low': [99, 100],
        'Close': [101, 102],
        'Adj Close': [101, 102],
        'Volume': [1000, 1100]
    }, index=dates)
    
    mock_ticker.history.return_value = df
    mock_ticker_class.return_value = mock_ticker
    
    res = provider.get_historical_prices("AAPL", date(2026, 1, 1), date(2026, 1, 2), "1d")
    assert res.symbol == "AAPL"
    assert len(res.data) == 2
    assert res.data[0].open == 100

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_historical_prices_empty_df_symbol_not_found(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()
    
    class MockFastInfo:
        @property
        def last_price(self):
            raise AttributeError("Mocked error")
            
    mock_ticker.fast_info = MockFastInfo()
    mock_ticker_class.return_value = mock_ticker
    
    with pytest.raises(SymbolNotFoundError):
        provider.get_historical_prices("INVALID", date(2026, 1, 1), date(2026, 1, 2), "1d")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_historical_prices_empty_df_valid_symbol(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()
    # fast_info works
    mock_ticker.fast_info.last_price = 100.0
    mock_ticker_class.return_value = mock_ticker
    
    res = provider.get_historical_prices("AAPL", date(2026, 1, 1), date(2026, 1, 2), "1d")
    assert res.symbol == "AAPL"
    assert len(res.data) == 0

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_historical_prices_exception(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.history.side_effect = Exception("API Error")
    mock_ticker_class.return_value = mock_ticker
    
    with pytest.raises(InvalidMarketDataError):
        provider.get_historical_prices("AAPL", date(2026, 1, 1), date(2026, 1, 2), "1d")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_company_profile_success(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.info = {
        'shortName': 'Apple Inc.',
        'exchange': 'NMS',
        'currency': 'USD',
        'sector': 'Technology',
        'industry': 'Consumer Electronics',
        'country': 'United States'
    }
    mock_ticker_class.return_value = mock_ticker
    
    profile = provider.get_company_profile("AAPL")
    assert profile.name == 'Apple Inc.'
    assert profile.sector == 'Technology'

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_company_profile_not_found(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mock_ticker_class.return_value = mock_ticker
    
    with pytest.raises(SymbolNotFoundError):
        provider.get_company_profile("INVALID")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_company_profile_exception(mock_ticker_class, provider):
    mock_ticker_class.side_effect = Exception("API error")
    with pytest.raises(InvalidMarketDataError):
        provider.get_company_profile("AAPL")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_financial_metrics_success(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.info = {
        'regularMarketPrice': 150.0,
        'marketCap': 2000000000,
        'trailingPE': 25.0,
        'trailingEps': 6.0,
        'dividendYield': 0.015,
        'beta': 1.2
    }
    mock_ticker_class.return_value = mock_ticker
    
    metrics = provider.get_financial_metrics("AAPL")
    assert metrics.pe_ratio == 25.0
    assert metrics.beta == 1.2

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_financial_metrics_not_found(mock_ticker_class, provider):
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mock_ticker_class.return_value = mock_ticker
    
    with pytest.raises(SymbolNotFoundError):
        provider.get_financial_metrics("INVALID")

@patch('app.providers.market.yahoo.yf.Ticker')
def test_get_financial_metrics_exception(mock_ticker_class, provider):
    mock_ticker_class.side_effect = Exception("API error")
    with pytest.raises(InvalidMarketDataError):
        provider.get_financial_metrics("AAPL")
