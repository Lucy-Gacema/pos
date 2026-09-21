from sqlalchemy.orm import Session

from app.models.payments import Payment
from app.repositories.base import commit_or_rollback


class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get(self, db: Session, id: int):
        return db.get(Payment, id)

    def get_all(self, db: Session):
        return db.query(Payment).all()

    def create(self, db: Session, data: dict):
        payment = Payment(**data)
        db.add(payment)
        commit_or_rollback(db)
        db.refresh(payment)
        return payment

    def update(self, db: Session, db_obj: Payment, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Payment):
        db.delete(db_obj)
        commit_or_rollback(db)


payment_repository = PaymentRepository()