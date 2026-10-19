from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id):
        statement = select(User).where(User.id == user_id)

        return self.db.scalar(statement)

    def get_by_username(self, username: str):
        statement = select(User).where(User.username == username)

        return self.db.scalar(statement)

    def get_by_email(self, email: str):
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def update_last_login(self, user: User) -> User:
        user.last_login_at = datetime.now(timezone.utc)
        self.db.flush()
        return user