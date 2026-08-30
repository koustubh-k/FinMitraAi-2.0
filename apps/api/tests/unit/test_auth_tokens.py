from datetime import timedelta

from jose import jwt

from app.auth.tokens import create_access_token, decode_access_token
from app.core.config import settings


def test_create_access_token():
    subject = "user123"
    token = create_access_token(subject)
    
    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    assert decoded["sub"] == subject
    assert "exp" in decoded

def test_create_access_token_with_delta():
    subject = "user123"
    delta = timedelta(minutes=15)
    token = create_access_token(subject, expires_delta=delta)
    
    decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    assert decoded["sub"] == subject
    assert "exp" in decoded

def test_decode_access_token():
    subject = "user123"
    token = create_access_token(subject)
    
    decoded_payload = decode_access_token(token)
    assert decoded_payload["sub"] == subject

def test_decode_access_token_invalid():
    decoded_sub = decode_access_token("invalid_token")
    assert decoded_sub is None
