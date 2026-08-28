import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.market_data import MarketDataService, get_market_data_service


# Mock service to inject during tests
def get_mock_market_data_service():
    return MarketDataService(provider_name="mock")

@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_market_data_service] = get_mock_market_data_service
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_api_get_quote_success():
    response = client.get("/api/v1/market/quote/RELIANCE")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE"
    assert data["price"] == 100.0
    assert "data_timestamp" in data

def test_api_get_quote_not_found():
    response = client.get("/api/v1/market/quote/INVALID")
    assert response.status_code == 404
    assert "Symbol not found" in response.json()["detail"]

def test_api_get_history():
    response = client.get("/api/v1/market/history/RELIANCE?start=2026-01-01&end=2026-01-05&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE"
    assert "data" in data
    assert len(data["data"]) == 5

def test_api_get_history_invalid_dates():
    # start > end
    response = client.get("/api/v1/market/history/RELIANCE?start=2026-01-10&end=2026-01-05")
    assert response.status_code == 422

def test_api_get_company_profile():
    response = client.get("/api/v1/market/company/TCS")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TCS"
    assert data["name"] == "TCS Corporation"

def test_api_get_financial_metrics():
    response = client.get("/api/v1/market/metrics/INFY")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "INFY"
    assert data["pe_ratio"] == 25.5

def test_api_get_history_default_dates():
    # Calling without start and end to hit lines 51, 53
    response = client.get("/api/v1/market/history/RELIANCE")
    assert response.status_code == 200
    assert "data" in response.json()

def test_handle_market_error_branches():
    from unittest.mock import MagicMock

    from app.core.errors import (
        InvalidMarketDataError,
        ProviderUnavailableError,
        RateLimitError,
    )
    
    # We will override the dependency temporarily for this test
    mock_service = MagicMock()
    app.dependency_overrides[get_market_data_service] = lambda: mock_service
    
    # Test RateLimitError
    mock_service.get_quote.side_effect = RateLimitError("Rate limit")
    response = client.get("/api/v1/market/quote/RATE")
    assert response.status_code == 429
    
    # Test ProviderUnavailableError
    mock_service.get_quote.side_effect = ProviderUnavailableError("Unavailable")
    response = client.get("/api/v1/market/quote/UNAVAIL")
    assert response.status_code == 503
    
    # Test InvalidMarketDataError
    mock_service.get_company_profile.side_effect = InvalidMarketDataError("Invalid")
    response = client.get("/api/v1/market/company/INVALID")
    assert response.status_code == 502
    
    # Test generic Exception
    mock_service.get_financial_metrics.side_effect = Exception("Generic")
    response = client.get("/api/v1/market/metrics/GENERIC")
    assert response.status_code == 500
    
    # Test get_history exceptions
    mock_service.get_historical_prices.side_effect = Exception("Generic history")
    response = client.get("/api/v1/market/history/GENERIC?start=2026-01-01&end=2026-01-05")
    assert response.status_code == 500
    
    # Restore dependency overrides
    app.dependency_overrides.clear()
    app.dependency_overrides[get_market_data_service] = get_mock_market_data_service
