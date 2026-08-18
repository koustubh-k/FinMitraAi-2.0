from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)


class PortfolioResponse(PortfolioBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
