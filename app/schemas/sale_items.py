from decimal import Decimal

from pydantic import BaseModel, ConfigDict, PositiveInt

from app.schemas.common import Money

class SaleItemCreate(BaseModel):
    sale_id: PositiveInt
    product_id: PositiveInt
    quantity: PositiveInt
    unit_price: Money


class SaleItemUpdate(BaseModel):
    sale_id: PositiveInt | None = None
    product_id: PositiveInt | None = None
    quantity: PositiveInt | None = None
    unit_price: Money | None = None


class SaleItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    sub_total: Decimal