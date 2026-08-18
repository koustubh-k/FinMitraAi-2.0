from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api import deps
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio import PortfolioService

router = APIRouter()


@router.get("/", response_model=list[PortfolioResponse])
def get_portfolios(
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
) -> Any:
    """
    Retrieve portfolios for a user.
    """
    return portfolio_service.get_user_portfolios(user_id=user_id, skip=skip, limit=limit)


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    user_id: UUID,
    portfolio_in: PortfolioCreate,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
) -> Any:
    """
    Create a new portfolio for a user.
    """
    return portfolio_service.create_portfolio(user_id=user_id, portfolio_in=portfolio_in)
