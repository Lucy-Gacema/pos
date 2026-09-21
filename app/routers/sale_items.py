from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.sale_items import SaleItemCreate, SaleItemUpdate, SaleItemResponse
from app.services.sale_items import SaleItemService

router = APIRouter(
    prefix="/sale-items",
    tags=["Sale Items"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return SaleItemService(db)


@router.post("/", response_model=SaleItemResponse, status_code=status.HTTP_201_CREATED)
def create_sale_item(p: SaleItemCreate, s: SaleItemService = Depends(get_srv)):
    return s.create_sale_item(p.model_dump())


@router.get("/", response_model=List[SaleItemResponse])
def read_sale_items(s: SaleItemService = Depends(get_srv)):
    return s.get_all_sale_items()


@router.get("/{id}", response_model=SaleItemResponse)
def read_sale_item(id: int, s: SaleItemService = Depends(get_srv)):
    return s.get_sale_item(id)


@router.put("/{id}", response_model=SaleItemResponse)
def update_sale_item(id: int, p: SaleItemUpdate, s: SaleItemService = Depends(get_srv)):
    return s.update_sale_item(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_sale_item(id: int, s: SaleItemService = Depends(get_srv)):
    s.delete_sale_item(id)
