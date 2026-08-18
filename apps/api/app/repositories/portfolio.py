from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.repositories.base import CRUDBase
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate


class CRUDPortfolio(CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100) -> list[Portfolio]:
        stmt = select(Portfolio).where(Portfolio.user_id == user_id).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
        
    def get_by_user_and_name(self, db: Session, *, user_id: UUID, name: str) -> Portfolio | None:
        stmt = select(Portfolio).where(Portfolio.user_id == user_id, Portfolio.name == name)
        return db.execute(stmt).scalar_one_or_none()


portfolio = CRUDPortfolio(Portfolio)
