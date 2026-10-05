from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.models.user import User


def permission(name: str):
    def decorator(func):
        setattr(func, "_permission", name)
        return func

    return decorator


def scan_permissions(app):
    discovered = set()

    for route in app.routes:
        endpoint = getattr(route, "endpoint", None)

        if endpoint is None:
            continue

        permission_name = getattr(
            endpoint,
            "_permission",
            None,
        )

        if permission_name:
            discovered.add(permission_name)

    return sorted(discovered)


def require_permission(name: str):
    async def checker(
        current_user: User = Depends(get_current_user),
    ):
        user_permissions = {
            permission.name
            for role in current_user.roles
            for permission in role.permissions
        }

        if name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {name}",
            )

        return current_user

    return checker