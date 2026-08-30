from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Quote(BaseModel):
    symbol: str
    price: float
    currency: str
    timestamp: datetime = Field(default_factory=utc_now)
    previous_close: float | None = None
    day_change: float | None = None
    day_change_percent: float | None = None
    data_timestamp: datetime = Field(default_factory=utc_now)
    retrieved_at: datetime = Field(default_factory=utc_now)

class HistoricalPrice(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float | None = None
    volume: int

class HistoricalPriceResponse(BaseModel):
    symbol: str
    interval: str
    data: list[HistoricalPrice]
    retrieved_at: datetime = Field(default_factory=utc_now)

class CompanyProfile(BaseModel):
    symbol: str
    name: str
    exchange: str | None = None
    currency: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    data_timestamp: datetime | None = None
    retrieved_at: datetime = Field(default_factory=utc_now)

class FinancialMetrics(BaseModel):
    symbol: str
    market_cap: float | None = None
    pe_ratio: float | None = None
    eps: float | None = None
    dividend_yield: float | None = None
    beta: float | None = None
    data_timestamp: datetime | None = None
    retrieved_at: datetime = Field(default_factory=utc_now)
