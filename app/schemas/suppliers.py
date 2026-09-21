from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.common import NonEmptyStr


class SupplierCreate(BaseModel):
    company_name: NonEmptyStr
    contact_name: NonEmptyStr
    phone_number: NonEmptyStr
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool = True


class SupplierUpdate(BaseModel):
    company_name: NonEmptyStr | None = None
    contact_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool | None = None


class SupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
    company_name: str
    contact_name: str
    phone_number: str
    email: str | None = None
    address: str | None = None
    is_active: bool
    