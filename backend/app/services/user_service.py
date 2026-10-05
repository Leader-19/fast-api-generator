from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.security_service import hash_password


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    def get_users(self, db: Session) -> list[User]:
        return self.user_repository.get_all(db)

    def get_user(
        self,
        db: Session,
        user_id: int,
    ) -> User:
        user = self.user_repository.get_by_id(db, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def create_user(
        self,
        db: Session,
        data: UserCreate,
    ) -> User:

        # Check duplicate email
        existing_user = self.user_repository.get_by_email(
            db,
            data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        # Get roles
        roles = self._get_roles(
            db,
            data.role_ids,
        )

        # Create user
        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            is_active=data.is_active,
            roles=roles,
        )

        return self.user_repository.create(db, user)

    def update_user(
        self,
        db: Session,
        user_id: int,
        data: UserUpdate,
    ) -> User:

        user = self.get_user(db, user_id)

        # Email
        if data.email is not None and data.email != user.email:

            existing_user = self.user_repository.get_by_email_except(
                db,
                data.email,
                user_id,
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )

            user.email = data.email

        # Name
        if data.name is not None:
            user.name = data.name

        # Active status
        if data.is_active is not None:
            user.is_active = data.is_active

        # Password
        if data.password:
            user.password_hash = hash_password(
                data.password
            )

        # Roles
        if data.role_ids is not None:
            roles = self._get_roles(
                db,
                data.role_ids,
            )

            user.roles = roles

        return self.user_repository.update(db, user)

    def delete_user(
        self,
        db: Session,
        user_id: int,
    ) -> None:

        user = self.get_user(db, user_id)

        # Prevent deleting ADMIN users
        admin_role = self.role_repository.get_by_name(
            db,
            "ADMIN",
        )

        if admin_role and admin_role in user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ADMIN users cannot be deleted",
            )

        self.user_repository.delete(db, user)

    def _get_roles(
        self,
        db: Session,
        role_ids: list[int] | None,
    ) -> list[Role]:

        if not role_ids:
            return []

        roles = self.role_repository.get_by_ids(
            db,
            role_ids,
        )

        if len(roles) != len(set(role_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more role IDs do not exist",
            )

        return roles