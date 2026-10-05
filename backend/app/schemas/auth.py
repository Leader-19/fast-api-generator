from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: "UserResponse"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    roles: list[str]
    permissions: list[str]

    model_config = {
        "from_attributes": True,
    }


LoginResponse.model_rebuild()