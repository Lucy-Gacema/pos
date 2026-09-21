from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sale_items import sale_item_repository


class SaleItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = sale_item_repository

    def get_sale_item(self, sale_item_id: int):
        sale_item = self.repository.get(self.db, sale_item_id)
        if not sale_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale item not found"
            )
        return sale_item

    def get_all_sale_items(self):
        return self.repository.get_all(self.db)

    def create_sale_item(self, data: dict):

        data["sub_total"] = data["quantity"] * data["unit_price"]
        return self.repository.create(self.db, data)

    def update_sale_item(self, sale_item_id: int, data: dict):
        sale_item = self.get_sale_item(sale_item_id)
        if "quantity" in data or "unit_price" in data:
            quantity = data.get("quantity", sale_item.quantity)
            unit_price = data.get("unit_price", sale_item.unit_price)
            data["sub_total"] = quantity * unit_price
        return self.repository.update(self.db, sale_item, data)

    def delete_sale_item(self, sale_item_id: int):
        sale_item = self.get_sale_item(sale_item_id)
        self.repository.delete(self.db, sale_item)
        return {"status": "success", "message": "Sale item deleted successfully"}