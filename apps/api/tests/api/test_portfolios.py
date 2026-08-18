import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.deps import get_portfolio_service
from app.main import app
from app.models.portfolio import Portfolio

client = TestClient(app)


def test_create_portfolio_success():
    mock_service = MagicMock()
    user_id = uuid.uuid4()
    portfolio_id = uuid.uuid4()
    mock_portfolio = Portfolio(
        id=portfolio_id,
        user_id=user_id,
        name="Tech Stocks",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_service.create_portfolio.return_value = mock_portfolio

    app.dependency_overrides[get_portfolio_service] = lambda: mock_service

    try:
        response = client.post(
            f"/api/v1/portfolios/?user_id={user_id}", 
            json={"name": "Tech Stocks"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tech Stocks"
        assert data["user_id"] == str(user_id)
        assert data["id"] == str(portfolio_id)
    finally:
        app.dependency_overrides.clear()


def test_get_portfolios_success():
    mock_service = MagicMock()
    user_id = uuid.uuid4()
    mock_portfolio = Portfolio(
        id=uuid.uuid4(),
        user_id=user_id,
        name="Tech Stocks",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_service.get_user_portfolios.return_value = [mock_portfolio]

    app.dependency_overrides[get_portfolio_service] = lambda: mock_service

    try:
        response = client.get(f"/api/v1/portfolios/?user_id={user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Tech Stocks"
        assert data[0]["user_id"] == str(user_id)
    finally:
        app.dependency_overrides.clear()
