from __future__ import annotations

import os

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.auth.dependencies import (
    get_current_user,
    require_permission,
)
from app.auth.permissions import permission
from app.database.connection import get_db
from app.models.user import User
from app.schemas.reconciliation import (
    PaginatedMatchesResponse,
    ReconciliationRunResponse,
    RunSummaryResponse,
)
from app.services.reconciliation_service import (
    ReconciliationService,
)


router = APIRouter(
    prefix="/api/reconciliation",
    tags=["Reconciliation"],
)


reconciliation_service = (
    ReconciliationService()
)


def cleanup_path(path: str | None) -> None:

    if not path:
        return

    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@router.get(
    "/runs",
    response_model=RunSummaryResponse,
    dependencies=[
        Depends(
            require_permission("reconciliation.view")
        ),
    ],
)
@permission("reconciliation.view")
def list_runs(
    db: Session = Depends(get_db),
) -> RunSummaryResponse:

    return (
        reconciliation_service.get_run_summary(
            db,
        )
    )


@router.get(
    "/runs/{run_id}",
    response_model=ReconciliationRunResponse,
    dependencies=[
        Depends(
            require_permission("reconciliation.view")
        ),
    ],
)
@permission("reconciliation.view")
def get_run(
    run_id: int,
    db: Session = Depends(get_db),
) -> ReconciliationRunResponse:

    run = reconciliation_service.get_run(
        db,
        run_id,
    )

    return (
        ReconciliationRunResponse.model_validate(
            run,
        )
    )


@router.get(
    "/runs/{run_id}/matches",
    response_model=PaginatedMatchesResponse,
    dependencies=[
        Depends(
            require_permission("reconciliation.view")
        ),
    ],
)
@permission("reconciliation.view")
def get_run_matches(
    run_id: int,
    status: str | None = Query(
        default=None,
        pattern="^(matched|mismatched|unmatched)$",
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PaginatedMatchesResponse:

    return (
        reconciliation_service.get_run_matches_page(
            db,
            run_id,
            status,
            page,
            page_size,
        )
    )


@router.get(
    "/runs/{run_id}/root-causes",
    dependencies=[
        Depends(
            require_permission("reconciliation.view")
        ),
    ],
)
@permission("reconciliation.view")
def get_run_root_causes(
    run_id: int,
    db: Session = Depends(get_db),
) -> list[dict]:

    return (
        reconciliation_service.get_run_root_causes(
            db,
            run_id,
        )
    )


@router.post(
    "/runs",
    response_model=ReconciliationRunResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "reconciliation.create"
            )
        ),
    ],
)
@permission("reconciliation.create")
async def create_run(
    name: str = Query(..., min_length=1),
    file_a: UploadFile = File(
        ...,
        description="Side A CSV (internal CDRs)",
    ),
    file_b: UploadFile = File(
        ...,
        description="Side B CSV (partner statement)",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReconciliationRunResponse:

    return (
        reconciliation_service.create_run(
            db,
            name=name,
            file_a=file_a,
            file_b=file_b,
            user_id=current_user.id,
        )
    )


@router.delete(
    "/runs/{run_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(
            require_permission(
                "reconciliation.delete"
            )
        ),
    ],
)
@permission("reconciliation.delete")
def delete_run(
    run_id: int,
    db: Session = Depends(get_db),
) -> None:

    reconciliation_service.delete_run(
        db,
        run_id,
    )

    return None
