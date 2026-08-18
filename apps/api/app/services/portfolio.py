from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import repositories
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate


class PortfolioService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_portfolios(self, user_id: UUID, skip: int = 0, limit: int = 100) -> list[Portfolio]:
        return repositories.portfolio.get_by_user_id(self.db, user_id=user_id, skip=skip, limit=limit)

    def create_portfolio(self, user_id: UUID, portfolio_in: PortfolioCreate) -> Portfolio:
        # Check if portfolio with same name already exists for this user
        existing_portfolio = repositories.portfolio.get_by_user_and_name(
            self.db, user_id=user_id, name=portfolio_in.name
        )
        if existing_portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A portfolio with this name already exists for this user.",
            )
            
        # Create dict explicitly injecting the user_id since it's not in PortfolioCreate
        obj_in_data = portfolio_in.model_dump()
        obj_in_data["user_id"] = user_id
        
        # We need to bypass the default CRUDBase create since it expects a Pydantic model directly mapping.
        # Alternatively we can just create the SQLAlchemy model here and use self.db
        
        db_obj = Portfolio(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
