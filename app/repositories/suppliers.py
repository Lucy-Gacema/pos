from sqlalchemy.orm import Session

from app.models.suppliers import Supplier
from app.repositories.base import commit_or_rollback


class SupplierRepository:
    def __init__(self):
        self.model = Supplier

    def get(self, db: Session, id: int):
        return db.get(Supplier, id)

    def get_all(self, db: Session):
        return db.query(Supplier).all()

    def create(self, db: Session, data: dict):
        supplier = Supplier(**data)
        db.add(supplier)
        commit_or_rollback(db)
        db.refresh(supplier)
        return supplier

    def update(self, db: Session, db_obj: Supplier, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Supplier):
        db.delete(db_obj)
        commit_or_rollback(db)


supplier_repository = SupplierRepository()