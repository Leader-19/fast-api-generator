from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    def get_all(self, db: Session) -> list[Role]:
        return db.scalars(
            select(Role).order_by(Role.id)
        ).all()

    def get_by_id(
        self,
        db: Session,
        role_id: int,
    ) -> Role | None:
        return db.get(Role, role_id)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> Role | None:
        return db.scalar(
            select(Role).where(
                Role.name == name
            )
        )

    def get_by_name_except(
        self,
        db: Session,
        name: str,
        role_id: int,
    ) -> Role | None:
        return db.scalar(
            select(Role).where(
                Role.name == name,
                Role.id != role_id,
            )
        )

    def create(
        self,
        db: Session,
        role: Role,
    ) -> Role:
        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    def update(
        self,
        db: Session,
        role: Role,
    ) -> Role:
        db.commit()
        db.refresh(role)

        return role

    def delete(
        self,
        db: Session,
        role: Role,
    ) -> None:
        db.delete(role)
        db.commit()