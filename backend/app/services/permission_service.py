from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.repositories.permission_repository import (
    PermissionRepository,
)


class PermissionService:

    def __init__(self):
        self.permission_repository = PermissionRepository()

    def get_permissions(
        self,
        db: Session,
    ) -> list[Permission]:
        return self.permission_repository.get_all(db)

    def get_permissions_by_ids(
        self,
        db: Session,
        permission_ids: list[int],
    ) -> list[Permission]:

        unique_ids = list(
            dict.fromkeys(permission_ids)
        )

        if not unique_ids:
            return []

        permissions = (
            self.permission_repository.get_by_ids(
                db,
                unique_ids,
            )
        )

        found_ids = {
            permission.id
            for permission in permissions
        }

        missing_ids = [
            permission_id
            for permission_id in unique_ids
            if permission_id not in found_ids
        ]

        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": (
                        "One or more permission IDs "
                        "do not exist"
                    ),
                    "missing_permission_ids": missing_ids,
                },
            )

        return permissions