import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class TransactionType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType, name="transactiontype"), nullable=False)
    
    quantity = Column(Numeric(precision=24, scale=8), nullable=False)
    price = Column(Numeric(precision=24, scale=8), nullable=False)
    
    transaction_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    portfolio = relationship("Portfolio", back_populates="transactions")

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('price >= 0', name='check_price_non_negative'),
    )
