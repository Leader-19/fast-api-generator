from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    permission_ids: list[int] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    permission_ids: list[int] | None = None


class RolePermissionAssign(BaseModel):
    permission_ids: list[int]


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None
    permissions: list[str] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }