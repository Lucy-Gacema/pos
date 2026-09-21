from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.users import user_repository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = user_repository

    def get_user(self, user_id: int):
        user = self.repository.get(self.db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    def get_all_users(self):
        return self.repository.get_all(self.db)

    def _ensure_username_free(self, username: str):
        if self.repository.get_by_username(self.db, username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

    def create_user(self, data: dict):
        self._ensure_username_free(data["username"])
        data["password_hash"] = hash_password(data.pop("password"))

        return self.repository.create(self.db, data)

    def update_user(self, user_id: int, data: dict):
        user = self.get_user(user_id)

        if "username" in data and data["username"] != user.username:
            self._ensure_username_free(data["username"])

        if "password" in data:
            data["password_hash"] = hash_password(data.pop("password"))

        return self.repository.update(self.db, user, data)

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.repository.delete(self.db, user)

        return {
            "status": "success",
            "message": "User deleted successfully"
        }