from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.suppliers import SupplierCreate, SupplierUpdate, SupplierResponse
from app.services.suppliers import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return SupplierService(db)


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(p: SupplierCreate, s: SupplierService = Depends(get_srv)):
    return s.create_supplier(p.model_dump())


@router.get("/", response_model=List[SupplierResponse])
def read_suppliers(s: SupplierService = Depends(get_srv)):
    return s.get_all_suppliers()


@router.get("/{id}", response_model=SupplierResponse)
def read_supplier(id: int, s: SupplierService = Depends(get_srv)):
    return s.get_supplier(id)


@router.put("/{id}", response_model=SupplierResponse)
def update_supplier(id: int, p: SupplierUpdate, s: SupplierService = Depends(get_srv)):
    return s.update_supplier(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_supplier(id: int, s: SupplierService = Depends(get_srv)):
    s.delete_supplier(id)
