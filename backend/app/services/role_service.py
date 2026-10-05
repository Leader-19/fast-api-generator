from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    RoleCreate,
    RolePermissionAssign,
    RoleUpdate,
)
from app.services.permission_service import PermissionService


class RoleService:

    def __init__(self):
        self.role_repository = RoleRepository()
        self.permission_service = PermissionService()

    def get_roles(
        self,
        db: Session,
    ) -> list[Role]:
        return self.role_repository.get_all(db)

    def get_role(
        self,
        db: Session,
        role_id: int,
    ) -> Role:

        role = self.role_repository.get_by_id(
            db,
            role_id,
        )

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found",
            )

        return role

    def create_role(
        self,
        db: Session,
        data: RoleCreate,
    ) -> Role:

        existing_role = (
            self.role_repository.get_by_name(
                db,
                data.name,
            )
        )

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role already exists",
            )

        permissions = (
            self.permission_service.get_permissions_by_ids(
                db,
                data.permission_ids,
            )
        )

        role = Role(
            name=data.name,
            description=data.description,
            permissions=permissions,
        )

        return self.role_repository.create(
            db,
            role,
        )

    def update_role(
        self,
        db: Session,
        role_id: int,
        data: RoleUpdate,
    ) -> Role:

        role = self.get_role(
            db,
            role_id,
        )

        # Update name
        if data.name is not None:

            existing_role = (
                self.role_repository.get_by_name_except(
                    db,
                    data.name,
                    role_id,
                )
            )

            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Role already exists",
                )

            role.name = data.name

        # Update description
        if data.description is not None:
            role.description = data.description

        # Update permissions
        if data.permission_ids is not None:

            permissions = (
                self.permission_service.get_permissions_by_ids(
                    db,
                    data.permission_ids,
                )
            )

            role.permissions = permissions

        return self.role_repository.update(
            db,
            role,
        )

    def assign_permissions(
        self,
        db: Session,
        role_id: int,
        data: RolePermissionAssign,
    ) -> Role:

        role = self.get_role(
            db,
            role_id,
        )

        permissions = (
            self.permission_service.get_permissions_by_ids(
                db,
                data.permission_ids,
            )
        )

        role.permissions = permissions

        return self.role_repository.update(
            db,
            role,
        )

    def delete_role(
        self,
        db: Session,
        role_id: int,
    ) -> None:

        role = self.get_role(
            db,
            role_id,
        )

        # Protect ADMIN role
        if role.name == "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ADMIN role cannot be deleted",
            )

        self.role_repository.delete(
            db,
            role,
        )