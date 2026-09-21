from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.categories import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return CategoryService(db)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(p: CategoryCreate, s: CategoryService = Depends(get_srv)):
    return s.create_category(p.model_dump())


@router.get("/", response_model=List[CategoryResponse])
def read_categories(s: CategoryService = Depends(get_srv)):
    return s.get_all_categories()


@router.get("/{id}", response_model=CategoryResponse)
def read_category(id: int, s: CategoryService = Depends(get_srv)):
    return s.get_category(id)


@router.put("/{id}", response_model=CategoryResponse)
def update_category(id: int, p: CategoryUpdate, s: CategoryService = Depends(get_srv)):
    return s.update_category(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_category(id: int, s: CategoryService = Depends(get_srv)):
    s.delete_category(id)
