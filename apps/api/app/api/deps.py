from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.portfolio import PortfolioService
from app.services.user import UserService


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:  # noqa: B008
    return UserService(db)


def get_portfolio_service(db: Session = Depends(get_db)) -> PortfolioService:  # noqa: B008
    return PortfolioService(db)



