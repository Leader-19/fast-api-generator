from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.auth.permissions import permission
from app.database.connection import get_db
from app.schemas.permission import PermissionResponse
from app.services.permission_service import PermissionService


router = APIRouter(
    prefix="/api/permissions",
    tags=["Permissions"],
)

permission_service = PermissionService()


@router.get(
    "",
    response_model=list[PermissionResponse],
    dependencies=[
        Depends(
            require_permission(
                "permissions.view"
            )
        )
    ],
)
@permission("permissions.view")
def list_permissions(
    db: Session = Depends(get_db),
):
    return permission_service.get_permissions(db)