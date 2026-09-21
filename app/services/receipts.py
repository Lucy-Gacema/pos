from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.receipts import receipt_repository


class ReceiptService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = receipt_repository

    def get_receipt(self, receipt_id: str):
        receipt = self.repository.get(self.db, receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receipt not found"
            )
        return receipt

    def get_all_receipts(self):
        return self.repository.get_all(self.db)

    def create_receipt(self, data: dict):
        return self.repository.create(self.db, data)

    def update_receipt(self, receipt_id: str, data: dict):
        receipt = self.get_receipt(receipt_id)
        return self.repository.update(self.db, receipt, data)

    def delete_receipt(self, receipt_id: str):
        receipt = self.get_receipt(receipt_id)
        self.repository.delete(self.db, receipt)
        return {"status": "success", "message": "Receipt deleted successfully"}