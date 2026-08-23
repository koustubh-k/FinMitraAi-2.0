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
