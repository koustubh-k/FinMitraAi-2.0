from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db.session import get_db
from app.main import app

client = TestClient(app)


def test_health_success():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "ok"}
    finally:
        app.dependency_overrides.clear()


def test_health_db_failure():
    mock_db = MagicMock()
    mock_db.execute.side_effect = OperationalError("connection failed", params={}, orig=Exception())
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        response = client.get("/health")
        assert response.status_code == 503
        assert response.json() == {"status": "ok", "database": "error"}
    finally:
        app.dependency_overrides.clear()
