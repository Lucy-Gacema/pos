from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, PositiveInt

from app.schemas.common import Money, NonEmptyStr


class SaleCreate(BaseModel):
    user_id: PositiveInt
    customer_id: PositiveInt | None = None
    total_amount: Money
    discount_amount: Money = Decimal("0.00")
    tax_amount: Money = Decimal("0.00")
    payment_status: NonEmptyStr
    receipt_number: NonEmptyStr
    sale_date: datetime


class SaleUpdate(BaseModel):
    user_id: PositiveInt | None = None
    customer_id: PositiveInt | None = None
    total_amount: Money | None = None
    discount_amount: Money | None = None
    tax_amount: Money | None = None
    payment_status: NonEmptyStr | None = None
    receipt_number: NonEmptyStr | None = None
    sale_date: datetime | None = None


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    user_id: int
    customer_id: int | None = None
    total_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    payment_status: str
    receipt_number: str
    sale_date: datetime