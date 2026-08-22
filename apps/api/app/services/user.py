from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import repositories
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: UUID) -> User | None:
        return repositories.user.get(self.db, id=user_id)
        
    def get_user_by_email(self, email: str) -> User | None:
        return repositories.user.get_by_email(self.db, email=email)

    def create_user(self, user_in: UserCreate) -> User:
        user = repositories.user.get_by_email(self.db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )
        return repositories.user.create(self.db, obj_in=user_in)
