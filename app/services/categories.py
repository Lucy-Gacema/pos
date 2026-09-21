from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.categories import category_repository


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = category_repository

    def get_category(self, category_id: int):
        category = self.repository.get(self.db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    def get_all_categories(self):
        return self.repository.get_all(self.db)

    def create_category(self, data: dict):
        return self.repository.create(self.db, data)

    def update_category(self, category_id: int, data: dict):
        category = self.get_category(category_id)
        return self.repository.update(self.db, category, data)

    def delete_category(self, category_id: int):
        category = self.get_category(category_id)
        self.repository.delete(self.db, category)
        return {"status": "success", "message": "Category deleted successfully"}