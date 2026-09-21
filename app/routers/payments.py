from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.payments import PaymentCreate, PaymentUpdate, PaymentResponse
from app.services.payments import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return PaymentService(db)


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(p: PaymentCreate, s: PaymentService = Depends(get_srv)):
    return s.create_payment(p.model_dump())


@router.get("/", response_model=List[PaymentResponse])
def read_payments(s: PaymentService = Depends(get_srv)):
    return s.get_all_payments()


@router.get("/{id}", response_model=PaymentResponse)
def read_payment(id: int, s: PaymentService = Depends(get_srv)):
    return s.get_payment(id)


@router.put("/{id}", response_model=PaymentResponse)
def update_payment(id: int, p: PaymentUpdate, s: PaymentService = Depends(get_srv)):
    return s.update_payment(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_payment(id: int, s: PaymentService = Depends(get_srv)):
    s.delete_payment(id)
