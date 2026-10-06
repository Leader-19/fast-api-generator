from __future__ import annotations

import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.auth.dependencies import (
    require_permission,
)
from app.auth.permissions import permission
from app.database.connection import get_db
from app.services.excel_service import (
    ExcelService,
)


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


excel_service = ExcelService()


def cleanup_path(path: str | None) -> None:

    if not path:
        return

    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@router.get(
    "/reconciliation/runs/{run_id}/excel",
    dependencies=[
        Depends(
            require_permission("reports.view")
        ),
    ],
)
@permission("reports.view")
def export_run_excel(
    run_id: int,
    db: Session = Depends(get_db),
) -> FileResponse:

    try:
        output_path = (
            excel_service.export_run_matches(
                db,
                run_id,
            )
        )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Report generation failed: "
                f"{exc}"
            ),
        )

    filename = os.path.basename(output_path)

    return FileResponse(
        path=output_path,
        filename=filename,
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        background=BackgroundTask(
            cleanup_path,
            output_path,
        ),
    )


@router.get(
    "/reconciliation/summary/excel",
    dependencies=[
        Depends(
            require_permission("reports.view")
        ),
    ],
)
@permission("reports.view")
def export_summary_excel(
    db: Session = Depends(get_db),
) -> FileResponse:

    try:
        output_path = (
            excel_service.export_summary(db)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Report generation failed: "
                f"{exc}"
            ),
        )

    return FileResponse(
        path=output_path,
        filename="reconciliation_summary.xlsx",
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        background=BackgroundTask(
            cleanup_path,
            output_path,
        ),
    )
