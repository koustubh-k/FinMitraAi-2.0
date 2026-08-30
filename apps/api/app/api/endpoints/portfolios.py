from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.financial import (
    AllocationResponse,
    HoldingResponse,
    PortfolioSummary,
    TransactionCreate,
    TransactionResponse,
)
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.market_data import MarketDataService, get_market_data_service
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


@router.post("/{portfolio_id}/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def add_transaction(
    portfolio_id: UUID,
    transaction_in: TransactionCreate,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    return portfolio_service.add_transaction(current_user.id, portfolio_id, transaction_in)

@router.get("/{portfolio_id}/transactions", response_model=list[TransactionResponse])
def get_transactions(
    portfolio_id: UUID,
    skip: int = 0,
    limit: int = 100,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    return portfolio_service.get_transactions(current_user.id, portfolio_id, skip=skip, limit=limit)

@router.get("/{portfolio_id}/holdings", response_model=list[HoldingResponse])
def get_holdings(
    portfolio_id: UUID,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    return portfolio_service.get_holdings(current_user.id, portfolio_id)

@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    portfolio_id: UUID,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    market_data_service: MarketDataService = Depends(get_market_data_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    return portfolio_service.get_portfolio_summary(current_user.id, portfolio_id, market_data_service)

@router.get("/{portfolio_id}/allocation", response_model=AllocationResponse)
def get_portfolio_allocation(
    portfolio_id: UUID,
    portfolio_service: PortfolioService = Depends(deps.get_portfolio_service),  # noqa: B008
    market_data_service: MarketDataService = Depends(get_market_data_service),  # noqa: B008
    current_user: User = Depends(get_current_user),
) -> Any:
    return portfolio_service.get_allocation(current_user.id, portfolio_id, market_data_service)
