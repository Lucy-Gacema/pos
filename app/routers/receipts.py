from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas.receipts import ReceiptCreate, ReceiptUpdate, ReceiptResponse
from app.services.receipts import ReceiptService

router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],
    dependencies=[Depends(get_current_user)],
)


def get_srv(db: Session = Depends(get_db)):
    return ReceiptService(db)


@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(p: ReceiptCreate, s: ReceiptService = Depends(get_srv)):
    return s.create_receipt(p.model_dump())


@router.get("/", response_model=List[ReceiptResponse])
def read_receipts(s: ReceiptService = Depends(get_srv)):
    return s.get_all_receipts()


@router.get("/{id}", response_model=ReceiptResponse)
def read_receipt(id: str, s: ReceiptService = Depends(get_srv)):
    return s.get_receipt(id)


@router.put("/{id}", response_model=ReceiptResponse)
def update_receipt(id: str, p: ReceiptUpdate, s: ReceiptService = Depends(get_srv)):
    return s.update_receipt(id, p.model_dump(exclude_none=True))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_receipt(id: str, s: ReceiptService = Depends(get_srv)):
    s.delete_receipt(id)
