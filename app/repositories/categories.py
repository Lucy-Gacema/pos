from sqlalchemy.orm import Session

from app.models.categories import Category
from app.repositories.base import commit_or_rollback


class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get(self, db: Session, id: int):
        return db.get(Category, id)

    def get_all(self, db: Session):
        return db.query(Category).all()

    def create(self, db: Session, data: dict):
        category = Category(**data)
        db.add(category)
        commit_or_rollback(db)
        db.refresh(category)
        return category

    def update(self, db: Session, db_obj: Category, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        commit_or_rollback(db)
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Category):
        db.delete(db_obj)
        commit_or_rollback(db)


category_repository = CategoryRepository()