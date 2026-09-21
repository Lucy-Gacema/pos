from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.suppliers import supplier_repository


class SupplierService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = supplier_repository

    def get_supplier(self, supplier_id: int):
        supplier = self.repository.get(self.db, supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
        return supplier

    def get_all_suppliers(self):
        return self.repository.get_all(self.db)

    def create_supplier(self, data: dict):
        return self.repository.create(self.db, data)

    def update_supplier(self, supplier_id: int, data: dict):
        supplier = self.get_supplier(supplier_id)
        return self.repository.update(self.db, supplier, data)

    def delete_supplier(self, supplier_id: int):
        supplier = self.get_supplier(supplier_id)
        self.repository.delete(self.db, supplier)
        return {"status": "success", "message": "Supplier deleted successfully"}