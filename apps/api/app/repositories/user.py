
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()


user = CRUDUser(User)
