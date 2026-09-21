from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.sales import SaleCreate, SaleUpdate, SaleResponse
from app.services.sales import SaleService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return SaleService(db)


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(p: SaleCreate, s: SaleService = Depends(get_srv)):
    return s.create_sale(p.model_dump())


@router.get("/", response_model=List[SaleResponse])
def read_sales(s: SaleService = Depends(get_srv)):
    return s.get_all_sales()


@router.get("/{id}", response_model=SaleResponse)
def read_sale(id: int, s: SaleService = Depends(get_srv)):
    return s.get_sale(id)


@router.put("/{id}", response_model=SaleResponse)
def update_sale(id: int, p: SaleUpdate, s: SaleService = Depends(get_srv)):
    return s.update_sale(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_sale(id: int, s: SaleService = Depends(get_srv)):
    s.delete_sale(id)
