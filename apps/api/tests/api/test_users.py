import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.deps import get_user_service
from app.auth.dependencies import get_current_user
from app.main import app
from app.models.user import User

client = TestClient(app)


def test_create_user_success():
    mock_service = MagicMock()
    user_id = uuid.uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_service.create_user.return_value = mock_user

    app.dependency_overrides[get_user_service] = lambda: mock_service

    try:
        response = client.post(
            "/api/v1/users/", 
            json={"email": "test@example.com", "password": "securepassword"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "password" not in data
    finally:
        app.dependency_overrides.clear()


def test_get_user_success():
    mock_service = MagicMock()
    user_id = uuid.uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    mock_service.get_user.return_value = mock_user

    app.dependency_overrides[get_user_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: User(id=user_id)

    try:
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["id"] == str(user_id)
    finally:
        app.dependency_overrides.clear()
