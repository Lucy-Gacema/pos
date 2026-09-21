from sqlalchemy.orm import Session

from app.models.products import Product
from app.repositories.base import commit_or_rollback


class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, id: int):
        return db.get(Product, id)

    def get_all(self, db: Session):
        return db.query(Product).all()

    def create(self, db: Session, data: dict):
        product = Product(**data)
        db.add(product)
        commit_or_rollback(db)
        db.refresh(product)
        return product

    def update(self, db: Session, db_obj: Product, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product):
        db.delete(db_obj)
        commit_or_rollback(db)


product_repository = ProductRepository()