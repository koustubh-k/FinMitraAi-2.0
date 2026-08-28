import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.auth.password import PasswordHasher
from app.auth.service import AuthService
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_user_service():
    service = MagicMock()
    return service

@pytest.fixture
def auth_service(mock_db, mock_user_service):
    service = AuthService(db=mock_db)
    service.user_service = mock_user_service
    return service

def test_register_success(auth_service, mock_db, mock_user_service):
    mock_user_service.get_user_by_email.return_value = None
    user_in = UserRegister(email="test@example.com", password="securepassword")
    
    user = auth_service.register(user_in)
    
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert PasswordHasher.verify_password("securepassword", user.password_hash)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_register_existing_email(auth_service, mock_user_service):
    mock_user_service.get_user_by_email.return_value = User(email="test@example.com")
    user_in = UserRegister(email="test@example.com", password="securepassword")
    
    with pytest.raises(HTTPException) as exc:
        auth_service.register(user_in)
    
    assert exc.value.status_code == 409

def test_register_short_password(auth_service, mock_user_service):
    mock_user_service.get_user_by_email.return_value = None
    user_in = UserRegister(email="test@example.com", password="short")
    
    with pytest.raises(HTTPException) as exc:
        auth_service.register(user_in)
    
    assert exc.value.status_code == 422

def test_login_success(auth_service, mock_user_service):
    pwd_hash = PasswordHasher.hash_password("securepassword")
    user = User(id=uuid.uuid4(), email="test@example.com", password_hash=pwd_hash, is_active=True)
    mock_user_service.get_user_by_email.return_value = user
    
    user_in = UserLogin(email="test@example.com", password="securepassword")
    token = auth_service.login(user_in)
    
    assert token.access_token is not None
    assert token.refresh_token is not None
    assert token.token_type == "bearer"

def test_login_invalid_password(auth_service, mock_user_service):
    pwd_hash = PasswordHasher.hash_password("securepassword")
    user = User(id=uuid.uuid4(), email="test@example.com", password_hash=pwd_hash, is_active=True)
    mock_user_service.get_user_by_email.return_value = user
    
    user_in = UserLogin(email="test@example.com", password="wrongpassword")
    with pytest.raises(HTTPException) as exc:
        auth_service.login(user_in)
    
    assert exc.value.status_code == 401

def test_login_inactive_user(auth_service, mock_user_service):
    pwd_hash = PasswordHasher.hash_password("securepassword")
    user = User(id=uuid.uuid4(), email="test@example.com", password_hash=pwd_hash, is_active=False)
    mock_user_service.get_user_by_email.return_value = user
    
    user_in = UserLogin(email="test@example.com", password="securepassword")
    with pytest.raises(HTTPException) as exc:
        auth_service.login(user_in)
    
    assert exc.value.status_code == 401

def test_refresh_success(auth_service, mock_db):
    user = User(id=uuid.uuid4(), email="test@example.com")
    db_token = RefreshToken(
        user_id=user.id,
        token_hash="dummy_hash", # Will be mocked
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        user=user
    )
    
    # Mock the query chain
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = db_token
    
    token = auth_service.refresh("sometoken")
    
    assert token.access_token is not None
    assert token.refresh_token is not None
    assert db_token.revoked_at is not None
    mock_db.commit.assert_called()

def test_refresh_invalid_token(auth_service, mock_db):
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        auth_service.refresh("sometoken")
    
    assert exc.value.status_code == 401
    assert "Invalid refresh token" in exc.value.detail

def test_refresh_revoked_token(auth_service, mock_db):
    db_token = RefreshToken(
        token_hash="dummy_hash",
        revoked_at=datetime.now(timezone.utc)
    )
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = db_token
    
    with pytest.raises(HTTPException) as exc:
        auth_service.refresh("sometoken")
    
    assert exc.value.status_code == 401
    assert "revoked" in exc.value.detail

def test_refresh_expired_token(auth_service, mock_db):
    db_token = RefreshToken(
        token_hash="dummy_hash",
        expires_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = db_token
    
    with pytest.raises(HTTPException) as exc:
        auth_service.refresh("sometoken")
    
    assert exc.value.status_code == 401
    assert "expired" in exc.value.detail

def test_logout(auth_service, mock_db):
    db_token = RefreshToken(
        token_hash="dummy_hash"
    )
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = db_token
    
    auth_service.logout("sometoken")
    
    assert db_token.revoked_at is not None
    mock_db.commit.assert_called()
