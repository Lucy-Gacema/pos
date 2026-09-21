from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, PositiveInt

from app.schemas.common import NonEmptyStr, PositiveMoney


class PaymentCreate(BaseModel):
    sale_id: PositiveInt
    payment_method: NonEmptyStr
    amount_paid: PositiveMoney
    payment_date: datetime


class PaymentUpdate(BaseModel):
    sale_id: PositiveInt | None = None
    payment_method: NonEmptyStr | None = None
    amount_paid: PositiveMoney | None = None
    payment_date: datetime | None = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    sale_id: int
    payment_method: str
    amount_paid: Decimal
    payment_date: datetime