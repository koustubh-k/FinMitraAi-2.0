from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Quote(BaseModel):
    symbol: str
    price: float
    currency: str
    timestamp: datetime
    previous_close: Optional[float] = None
    day_change: Optional[float] = None
    day_change_percent: Optional[float] = None
    data_timestamp: datetime
    retrieved_at: datetime = Field(default_factory=utc_now)

class HistoricalPrice(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    adjusted_close: Optional[float] = None
    volume: int

class HistoricalPriceResponse(BaseModel):
    symbol: str
    interval: str
    data: List[HistoricalPrice]
    retrieved_at: datetime = Field(default_factory=utc_now)

class CompanyProfile(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    currency: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    data_timestamp: Optional[datetime] = None
    retrieved_at: datetime = Field(default_factory=utc_now)

class FinancialMetrics(BaseModel):
    symbol: str
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    data_timestamp: Optional[datetime] = None
    retrieved_at: datetime = Field(default_factory=utc_now)
