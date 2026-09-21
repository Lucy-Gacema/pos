from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import NonEmptyStr

Role = Literal["admin", "cashier"]



class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    first_name: NonEmptyStr
    last_name: NonEmptyStr


class UserCreate(UserRegister):
    role: Role = "cashier"


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    role: Role | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool