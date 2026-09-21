from pydantic import BaseModel, ConfigDict

from app.schemas.common import NonEmptyStr


class CategoryCreate(BaseModel):
    category_name: NonEmptyStr
    is_active: bool = True


class CategoryUpdate(BaseModel):
    category_name: NonEmptyStr | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    category_name: str
    is_active: bool