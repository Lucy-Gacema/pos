from sqlalchemy.orm import Session

from app.models.sales import Sale
from app.repositories.base import commit_or_rollback


class SaleRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, id: int):
        return db.get(Sale, id)

    def get_all(self, db: Session):
        return db.query(Sale).all()

    def create(self, db: Session, data: dict):
        sale = Sale(**data)
        db.add(sale)
        commit_or_rollback(db)
        db.refresh(sale)
        return sale

    def update(self, db: Session, db_obj: Sale, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale):
        db.delete(db_obj)
        commit_or_rollback(db)


sale_repository = SaleRepository()