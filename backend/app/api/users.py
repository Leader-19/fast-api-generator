from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.auth.permissions import permission
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)

user_service = UserService()


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        roles=[role.name for role in user.roles],
    )


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[
        Depends(require_permission("users.view"))
    ],
)
@permission("users.view")
def get_users(
    db: Session = Depends(get_db),
):
    users = user_service.get_users(db)

    return [
        user_to_response(user)
        for user in users
    ]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("users.create"))
    ],
)
@permission("users.create")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    user = user_service.create_user(
        db,
        data,
    )

    return user_to_response(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[
        Depends(require_permission("users.view"))
    ],
)
@permission("users.view")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = user_service.get_user(
        db,
        user_id,
    )

    return user_to_response(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[
        Depends(require_permission("users.update"))
    ],
)
@permission("users.update")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = user_service.update_user(
        db,
        user_id,
        data,
    )

    return user_to_response(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("users.delete"))
    ],
)
@permission("users.delete")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user_service.delete_user(
        db,
        user_id,
    )

    return None
