from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    role_ids: list[int] = []


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    role_ids: list[int] | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    roles: list[str]

    model_config = {"from_attributes": True}