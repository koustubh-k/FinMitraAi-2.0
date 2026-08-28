import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol = Column(String, nullable=False)
    
    quantity = Column(Numeric(precision=24, scale=8), nullable=False)
    average_cost = Column(Numeric(precision=24, scale=8), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")

    __table_args__ = (
        UniqueConstraint('portfolio_id', 'symbol', name='uix_holding_portfolio_symbol'),
        CheckConstraint('quantity >= 0', name='check_holding_quantity_non_negative'),
        CheckConstraint('average_cost >= 0', name='check_holding_cost_non_negative'),
    )
