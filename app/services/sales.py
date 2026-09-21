from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sales import sale_repository


class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = sale_repository

    def get_sale(self, sale_id: int):
        sale = self.repository.get(self.db, sale_id)
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found"
            )
        return sale

    def get_all_sales(self):
        return self.repository.get_all(self.db)

    def create_sale(self, data: dict):
        return self.repository.create(self.db, data)

    def update_sale(self, sale_id: int, data: dict):
        sale = self.get_sale(sale_id)
        return self.repository.update(self.db, sale, data)

    def delete_sale(self, sale_id: int):
        sale = self.get_sale(sale_id)
        self.repository.delete(self.db, sale)
        return {"status": "success", "message": "Sale deleted successfully"}