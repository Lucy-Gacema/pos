from decimal import Decimal

from pydantic import BaseModel, ConfigDict, NonNegativeInt, PositiveInt

from app.schemas.common import NonEmptyStr, PositiveMoney


class ProductCreate(BaseModel):
    product_name: NonEmptyStr
    barcode: NonEmptyStr
    category_id: PositiveInt
    selling_price: PositiveMoney
    reorder_level: NonNegativeInt
    in_stock: NonNegativeInt
    supplier_id: PositiveInt


class ProductUpdate(BaseModel):
    product_name: NonEmptyStr | None = None
    barcode: NonEmptyStr | None = None
    category_id: PositiveInt | None = None
    selling_price: PositiveMoney | None = None
    reorder_level: NonNegativeInt | None = None
    in_stock: NonNegativeInt | None = None
    supplier_id: PositiveInt | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    barcode: str
    category_id: int
    selling_price: Decimal
    reorder_level: int
    in_stock: int
    supplier_id: int