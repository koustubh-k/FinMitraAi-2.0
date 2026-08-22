from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(deps.get_user_service),  # noqa: B008
) -> Any:
    """
    Create new user.
    """
    return user_service.create_user(user_in=user_in)





@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(deps.get_user_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific user by ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
        
    user = user_service.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
