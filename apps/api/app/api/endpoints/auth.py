from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.auth.dependencies import get_current_user
from app.auth.service import AuthService
from app.models.user import User
from app.schemas.auth import RefreshTokenRequest, Token, UserLogin, UserRegister
from app.schemas.user import UserResponse

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """
    Register a new user.
    """
    return auth_service.register(user_in=user_in)


@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """
    Login user.
    """
    return auth_service.login(user_in=user_in)


@router.post("/refresh", response_model=Token)
def refresh(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """
    Refresh access token.
    """
    return auth_service.refresh(refresh_token=request.refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    """
    Logout user (revoke refresh token).
    """
    auth_service.logout(refresh_token=request.refresh_token)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
