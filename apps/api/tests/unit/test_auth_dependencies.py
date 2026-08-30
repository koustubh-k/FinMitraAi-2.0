import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.auth.dependencies import get_current_user
from app.models.user import User


@pytest.fixture
def mock_user_service():
    return MagicMock()

@patch("app.auth.dependencies.decode_access_token")
def test_get_current_user_success(mock_decode, mock_user_service):
    user_id = str(uuid.uuid4())
    mock_decode.return_value = {"sub": user_id}
    
    mock_user = User(id=uuid.UUID(user_id), is_active=True)
    mock_user_service.get_user.return_value = mock_user
    
    user = get_current_user(token="valid_token", user_service=mock_user_service)
    
    assert user.id == mock_user.id
    assert user.is_active is True

@patch("app.auth.dependencies.decode_access_token")
def test_get_current_user_invalid_token(mock_decode, mock_user_service):
    mock_decode.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="invalid_token", user_service=mock_user_service)
    
    assert exc.value.status_code == 401

@patch("app.auth.dependencies.decode_access_token")
def test_get_current_user_missing_sub(mock_decode, mock_user_service):
    mock_decode.return_value = {"other": "data"}
    
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="valid_token_no_sub", user_service=mock_user_service)
    
    assert exc.value.status_code == 401

@patch("app.auth.dependencies.decode_access_token")
def test_get_current_user_not_found(mock_decode, mock_user_service):
    user_id = str(uuid.uuid4())
    mock_decode.return_value = {"sub": user_id}
    
    mock_user_service.get_user.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="valid_token", user_service=mock_user_service)
    
    assert exc.value.status_code == 401

@patch("app.auth.dependencies.decode_access_token")
def test_get_current_user_inactive(mock_decode, mock_user_service):
    user_id = str(uuid.uuid4())
    mock_decode.return_value = {"sub": user_id}
    
    mock_user = User(id=uuid.UUID(user_id), is_active=False)
    mock_user_service.get_user.return_value = mock_user
    
    with pytest.raises(HTTPException) as exc:
        get_current_user(token="valid_token", user_service=mock_user_service)
    
    assert exc.value.status_code == 400
    assert "Inactive user" in exc.value.detail
