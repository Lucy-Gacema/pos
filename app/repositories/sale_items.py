from sqlalchemy.orm import Session

from app.models.sale_items import SaleItem
from app.repositories.base import commit_or_rollback


class SaleItemRepository:
    def __init__(self):
        self.model = SaleItem

    def get(self, db: Session, id: int):
        return db.get(SaleItem, id)

    def get_all(self, db: Session):
        return db.query(SaleItem).all()

    def create(self, db: Session, data: dict):
        sale_item = SaleItem(**data)
        db.add(sale_item)
        commit_or_rollback(db)
        db.refresh(sale_item)
        return sale_item

    def update(self, db: Session, db_obj: SaleItem, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SaleItem):
        db.delete(db_obj)
        commit_or_rollback(db)


sale_item_repository = SaleItemRepository()