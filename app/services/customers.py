from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customers import customer_repository


class CustomerService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = customer_repository

    def get_customer(self, customer_id: int):
        customer = self.repository.get(self.db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return customer

    def get_all_customers(self):
        return self.repository.get_all(self.db)

    def create_customer(self, data: dict):
        return self.repository.create(self.db, data)

    def update_customer(self, customer_id: int, data: dict):
        customer = self.get_customer(customer_id)
        return self.repository.update(self.db, customer, data)

    def delete_customer(self, customer_id: int):
        customer = self.get_customer(customer_id)
        self.repository.delete(self.db, customer)
        return {"status": "success", "message": "Customer deleted successfully"}