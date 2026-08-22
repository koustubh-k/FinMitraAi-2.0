from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.password import PasswordHasher
from app.auth.tokens import create_access_token
from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserCreate
from app.services.user import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def register(self, user_in: UserRegister) -> User:
        if self.user_service.get_user_by_email(email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Validate password manually since schema validation is passed
        if len(user_in.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 8 characters long"
            )
            
        password_hash = PasswordHasher.hash_password(user_in.password)
        
        user = User(
            email=user_in.email,
            password_hash=password_hash,
            is_active=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, user_in: UserLogin) -> Token:
        user = self.user_service.get_user_by_email(email=user_in.email)
        if not user or not PasswordHasher.verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is inactive"
            )

        return self._issue_tokens(user)
        
    def refresh(self, refresh_token: str) -> Token:
        token_hash = PasswordHasher.hash_password(refresh_token) # we need a secure hash for the refresh token
        
        # Actually it's better to use something simpler like SHA256 for fast lookup, or just Argon2. 
        # But Argon2 generates a new salt each time, so looking up by hash won't work with Argon2 directly 
        # unless we compare all tokens (slow). Let's use SHA256 for refresh token storage.
        import hashlib
        m = hashlib.sha256()
        m.update(refresh_token.encode('utf-8'))
        token_hash = m.hexdigest()
        
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
            
        if db_token.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token revoked"
            )
            
        if db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
            
        user = db_token.user
        
        # Revoke the old token (rotation)
        db_token.revoked_at = datetime.now(timezone.utc)
        self.db.commit()
        
        return self._issue_tokens(user)
        
    def logout(self, refresh_token: str) -> None:
        import hashlib
        m = hashlib.sha256()
        m.update(refresh_token.encode('utf-8'))
        token_hash = m.hexdigest()
        
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        if db_token and db_token.revoked_at is None:
            db_token.revoked_at = datetime.now(timezone.utc)
            self.db.commit()

    def _issue_tokens(self, user: User) -> Token:
        access_token = create_access_token(subject=str(user.id))
        
        import secrets
        import hashlib
        raw_refresh_token = secrets.token_urlsafe(32)
        
        m = hashlib.sha256()
        m.update(raw_refresh_token.encode('utf-8'))
        token_hash = m.hexdigest()
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        
        db_token = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(db_token)
        self.db.commit()
        
        return Token(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
