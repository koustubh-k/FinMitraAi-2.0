from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone, timedelta
import uuid

from app.main import app
from app.api.endpoints.auth import get_auth_service
from app.auth.dependencies import get_current_user
from app.auth.password import PasswordHasher
from app.models.user import User

client = TestClient(app)

@pytest.fixture
def mock_auth_service():
    mock_service = MagicMock()
    app.dependency_overrides[get_auth_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()

def test_register_success(mock_auth_service):
    user_id = uuid.uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_auth_service.register.return_value = mock_user
    
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "securepassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_login_success(mock_auth_service):
    from app.schemas.auth import Token
    mock_auth_service.login.return_value = Token(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
        expires_in=900
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "access"
    assert data["refresh_token"] == "refresh"

def test_auth_me():
    user_id = uuid.uuid4()
    mock_user = User(
        id=user_id, 
        email="test@example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    try:
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
    finally:
        app.dependency_overrides.clear()
