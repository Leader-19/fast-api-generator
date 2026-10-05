from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.services.security_service import verify_password


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def login(
        self,
        db: Session,
        data: LoginRequest,
    ):

        user = self.user_repository.get_by_email(
            db,
            data.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        token = create_access_token(user.id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": self._user_to_dict(user),
        }

    def get_current_user_response(
        self,
        current_user: User,
    ):
        return self._user_to_dict(current_user)

    def _user_to_dict(
        self,
        user: User,
    ):
        roles = [
            role.name
            for role in user.roles
        ]

        permissions = sorted({
            permission.name
            for role in user.roles
            for permission in role.permissions
        })

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "roles": roles,
            "permissions": permissions,
        }