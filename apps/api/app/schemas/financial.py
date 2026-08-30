from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    symbol: str = Field(..., min_length=1)
    transaction_type: TransactionType
    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., ge=0)
    transaction_date: datetime

class TransactionResponse(BaseModel):
    id: UUID
    portfolio_id: UUID
    symbol: str
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    transaction_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class HoldingResponse(BaseModel):
    id: UUID
    portfolio_id: UUID
    symbol: str
    quantity: Decimal
    average_cost: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PositionAllocation(BaseModel):
    symbol: str
    market_value: Decimal | None
    weight_percentage: Decimal | None
    valuation_status: str = "AVAILABLE"

class PositionSummary(BaseModel):
    symbol: str
    quantity: Decimal
    average_cost: Decimal
    cost_basis: Decimal
    market_price: Decimal | None
    market_value: Decimal | None
    realized_pnl: Decimal
    unrealized_pnl: Decimal | None
    total_pnl: Decimal | None
    valuation_status: str = "AVAILABLE"

class PortfolioSummary(BaseModel):
    portfolio_id: UUID
    market_value: Decimal | None
    cost_basis: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal | None
    total_pnl: Decimal | None
    return_percentage: Decimal | None
    positions: list[PositionSummary]

class AllocationResponse(BaseModel):
    positions: list[PositionAllocation]
