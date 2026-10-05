from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.auth.permissions import permission
from app.database.connection import get_db
from app.models.role import Role
from app.schemas.role import (
    RoleCreate,
    RolePermissionAssign,
    RoleResponse,
    RoleUpdate,
)
from app.services.role_service import RoleService


router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"],
)

role_service = RoleService()


def role_to_response(
    role: Role,
) -> RoleResponse:
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=[
            permission.name
            for permission in role.permissions
        ],
    )


@router.get(
    "",
    response_model=list[RoleResponse],
    dependencies=[
        Depends(
            require_permission("roles.view")
        )
    ],
)
@permission("roles.view")
def list_roles(
    db: Session = Depends(get_db),
):
    roles = role_service.get_roles(db)

    return [
        role_to_response(role)
        for role in roles
    ]


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission("roles.create")
        )
    ],
)
@permission("roles.create")
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
):
    role = role_service.create_role(
        db,
        data,
    )

    return role_to_response(role)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[
        Depends(
            require_permission("roles.view")
        )
    ],
)
@permission("roles.view")
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    role = role_service.get_role(
        db,
        role_id,
    )

    return role_to_response(role)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[
        Depends(
            require_permission("roles.update")
        )
    ],
)
@permission("roles.update")
def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
):
    role = role_service.update_role(
        db,
        role_id,
        data,
    )

    return role_to_response(role)


@router.post(
    "/{role_id}/permissions",
    response_model=RoleResponse,
    dependencies=[
        Depends(
            require_permission("roles.update")
        )
    ],
)
@permission("roles.update")
def assign_permissions_to_role(
    role_id: int,
    data: RolePermissionAssign,
    db: Session = Depends(get_db),
):
    role = role_service.assign_permissions(
        db,
        role_id,
        data,
    )

    return role_to_response(role)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission("roles.delete")
        )
    ],
)
@permission("roles.delete")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    role_service.delete_role(
        db,
        role_id,
    )

    return None