from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_user,
    require_permission,
)
from app.auth.permissions import permission
from app.database.connection import get_db
from app.models.user import User
from app.schemas.reconciliation import (
    InvestigationCaseResponse,
    InvestigationCaseUpdate,
)
from app.services.investigation_service import (
    InvestigationService,
)


router = APIRouter(
    prefix="/api/investigations",
    tags=["Investigations"],
)


investigation_service = (
    InvestigationService()
)


@router.get(
    "",
    response_model=list[InvestigationCaseResponse],
    dependencies=[
        Depends(
            require_permission(
                "investigation.view"
            )
        ),
    ],
)
@permission("investigation.view")
def list_cases(
    run_id: int | None = Query(default=None),
    case_status: str | None = Query(
        default=None,
        pattern="^(open|in_progress|resolved|closed)$",
    ),
    db: Session = Depends(get_db),
) -> list[InvestigationCaseResponse]:

    cases = (
        investigation_service.get_cases(
            db,
            run_id,
            case_status,
        )
    )

    return [
        InvestigationCaseResponse.model_validate(
            case,
        )
        for case in cases
    ]


@router.get(
    "/{case_id}",
    response_model=InvestigationCaseResponse,
    dependencies=[
        Depends(
            require_permission(
                "investigation.view"
            )
        ),
    ],
)
@permission("investigation.view")
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
) -> InvestigationCaseResponse:

    case = investigation_service.get_case(
        db,
        case_id,
    )

    return (
        InvestigationCaseResponse.model_validate(
            case,
        )
    )


@router.post(
    "",
    response_model=InvestigationCaseResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_permission(
                "investigation.create"
            )
        ),
    ],
)
@permission("investigation.create")
def create_case(
    match_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InvestigationCaseResponse:

    case = (
        investigation_service.create_case(
            db,
            match_id=match_id,
            user_id=current_user.id,
        )
    )

    return (
        InvestigationCaseResponse.model_validate(
            case,
        )
    )


@router.put(
    "/{case_id}",
    response_model=InvestigationCaseResponse,
    dependencies=[
        Depends(
            require_permission(
                "investigation.update"
            )
        ),
    ],
)
@permission("investigation.update")
def update_case(
    case_id: int,
    data: InvestigationCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InvestigationCaseResponse:

    case = (
        investigation_service.update_case(
            db,
            case_id,
            data,
            user_id=current_user.id,
        )
    )

    return (
        InvestigationCaseResponse.model_validate(
            case,
        )
    )
