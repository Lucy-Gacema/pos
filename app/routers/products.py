from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.services.products import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return ProductService(db)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(p: ProductCreate, s: ProductService = Depends(get_srv)):
    return s.create_product(p.model_dump())


@router.get("/", response_model=List[ProductResponse])
def read_products(s: ProductService = Depends(get_srv)):
    return s.get_all_products()


@router.get("/{id}", response_model=ProductResponse)
def read_product(id: int, s: ProductService = Depends(get_srv)):
    return s.get_product(id)


@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, p: ProductUpdate, s: ProductService = Depends(get_srv)):
    return s.update_product(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_product(id: int, s: ProductService = Depends(get_srv)):
    s.delete_product(id)
