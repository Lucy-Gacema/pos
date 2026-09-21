from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_admin)],
)


def get_srv(db: Session = Depends(get_db)):
    return UserService(db)


@router.get("/", response_model=List[UserResponse])
def read_users(s: UserService = Depends(get_srv)):
    return s.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, s: UserService = Depends(get_srv)):
    return s.get_user(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, s: UserService = Depends(get_srv)):
    return s.create_user(data.model_dump())


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, s: UserService = Depends(get_srv)):
    return s.update_user(user_id, data.model_dump(exclude_none=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, s: UserService = Depends(get_srv)):
    s.delete_user(user_id)
