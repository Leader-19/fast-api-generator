from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:

    def get_all(
        self,
        db: Session,
    ) -> list[Permission]:
        return db.scalars(
            select(Permission).order_by(
                Permission.name
            )
        ).all()

    def get_by_ids(
        self,
        db: Session,
        permission_ids: list[int],
    ) -> list[Permission]:

        unique_ids = list(
            dict.fromkeys(permission_ids)
        )

        if not unique_ids:
            return []

        return db.scalars(
            select(Permission).where(
                Permission.id.in_(unique_ids)
            )
        ).all()