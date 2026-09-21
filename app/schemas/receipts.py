from pydantic import BaseModel, ConfigDict

from app.schemas.common import NonEmptyStr


class ReceiptCreate(BaseModel):
    receipt_number: NonEmptyStr
    is_printed: bool = False


class ReceiptUpdate(BaseModel):
   
    is_printed: bool | None = None


class ReceiptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receipt_number: str
    is_printed: bool