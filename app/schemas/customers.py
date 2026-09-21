from pydantic import BaseModel, ConfigDict, EmailStr, NonNegativeInt

from app.schemas.common import NonEmptyStr


class CustomerCreate(BaseModel):
    first_name: NonEmptyStr
    last_name: NonEmptyStr | None = None  # optional, like the database column
    phone_number: NonEmptyStr
    email: EmailStr | None = None
    points: NonNegativeInt = 0


class CustomerUpdate(BaseModel):
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    email: EmailStr | None = None
    points: NonNegativeInt | None = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    first_name: str
    last_name: str | None = None
    phone_number: str
    email: str | None = None
    points: int