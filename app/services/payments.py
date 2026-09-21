from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.payments import payment_repository


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = payment_repository

    def get_payment(self, payment_id: int):
        payment = self.repository.get(self.db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        return payment

    def get_all_payments(self):
        return self.repository.get_all(self.db)

    def create_payment(self, data: dict):
        return self.repository.create(self.db, data)

    def update_payment(self, payment_id: int, data: dict):
        payment = self.get_payment(payment_id)
        return self.repository.update(self.db, payment, data)

    def delete_payment(self, payment_id: int):
        payment = self.get_payment(payment_id)
        self.repository.delete(self.db, payment)
        return {"status": "success", "message": "Payment deleted successfully"}