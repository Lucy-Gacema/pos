from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.customers import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customers import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return CustomerService(db)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(p: CustomerCreate, s: CustomerService = Depends(get_srv)):
    return s.create_customer(p.model_dump())


@router.get("/", response_model=List[CustomerResponse])
def read_customers(s: CustomerService = Depends(get_srv)):
    return s.get_all_customers()


@router.get("/{id}", response_model=CustomerResponse)
def read_customer(id: int, s: CustomerService = Depends(get_srv)):
    return s.get_customer(id)


@router.put("/{id}", response_model=CustomerResponse)
def update_customer(id: int, p: CustomerUpdate, s: CustomerService = Depends(get_srv)):
    return s.update_customer(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_customer(id: int, s: CustomerService = Depends(get_srv)):
    s.delete_customer(id)
