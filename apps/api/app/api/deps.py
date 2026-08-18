from collections.abc import Generator
from uuid import UUID

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


# Dummy auth dependency for Phase 1 testing
def get_current_user_id() -> UUID:
    """
    Dummy authentication dependency.
    In a real app, this would verify a JWT token and return the authenticated user's ID.
    For Phase 1, it expects the client to pass the user ID if we need to mock it,
    or we can just hardcode a known UUID if we wanted, but to make it testable,
    we'll raise a NotImplementedError if used directly without override, or we can
    just return a static UUID. 
    Actually, let's extract it from a header or just return a dummy UUID.
    For Phase 1, we will allow tests to override this, or endpoints can take user_id as a parameter.
    """
    # For now, we will require the user_id as a query parameter or path parameter 
    # instead of a proper auth token, just to keep Phase 1 simple.
