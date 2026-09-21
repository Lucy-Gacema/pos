from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.products import product_repository


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = product_repository

    def get_product(self, product_id: int):
        product = self.repository.get(self.db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    def get_all_products(self):
        return self.repository.get_all(self.db)

    def create_product(self, data: dict):
        return self.repository.create(self.db, data)

    def update_product(self, product_id: int, data: dict):
        product = self.get_product(product_id)
        return self.repository.update(self.db, product, data)

    def delete_product(self, product_id: int):
        product = self.get_product(product_id)
        self.repository.delete(self.db, product)
        return {"status": "success", "message": "Product deleted successfully"}