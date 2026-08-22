from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio import PortfolioService

router = APIRouter()


@router.get("/", response_model=list[PortfolioResponse])
def get_portfolios(
    user_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve portfolios for a user.
    """
    # Enforce resource ownership
    target_user_id = user_id or current_user.id
    if target_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    
    return portfolio_service.get_user_portfolios(user_id=target_user_id, skip=skip, limit=limit)


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_in: PortfolioCreate,
    user_id: UUID | None = None,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new portfolio for a user.
    """
    target_user_id = user_id or current_user.id
    if target_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
        
    return portfolio_service.create_portfolio(user_id=target_user_id, portfolio_in=portfolio_in)

