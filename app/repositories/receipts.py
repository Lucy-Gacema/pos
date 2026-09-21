from sqlalchemy.orm import Session

from app.models.receipts import Receipt
from app.repositories.base import commit_or_rollback


class ReceiptRepository:
    def __init__(self):
        self.model = Receipt

    def get(self, db: Session, id: str):
        return db.get(Receipt, id)

    def get_all(self, db: Session):
        return db.query(Receipt).all()

    def create(self, db: Session, data: dict):
        receipt = Receipt(**data)
        db.add(receipt)
        commit_or_rollback(db)
        db.refresh(receipt)
        return receipt

    def update(self, db: Session, db_obj: Receipt, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Receipt):
        db.delete(db_obj)
        commit_or_rollback(db)


receipt_repository = ReceiptRepository()