from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.users import user_repository
from app.services.users import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = user_repository

    def register(self, data: dict):
        data["role"] = "cashier" if self.repository.get_all(self.db) else "admin"
        return UserService(self.db).create_user(data)

    def authenticate(self, username: str, password: str):
        user = self.repository.get_by_username(self.db, username)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive",
            )

        return user

    def login(self, username: str, password: str) -> dict:
        user = self.authenticate(username, password)
        return {
            "access_token": create_access_token(user_id=user.user_id),
            "token_type": "bearer",
        }
