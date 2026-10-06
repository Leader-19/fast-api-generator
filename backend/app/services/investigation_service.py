from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reconciliation import (
    InvestigationCase,
    ReconciliationMatch,
)
from app.repositories.reconciliation_repository import (
    ReconciliationRepository,
)
from app.schemas.reconciliation import (
    InvestigationCaseUpdate,
)


ALLOWED_STATUSES = [
    "open",
    "in_progress",
    "resolved",
    "closed",
]


class InvestigationService:

    def __init__(self):
        self.repository = (
            ReconciliationRepository()
        )

    def get_cases(
        self,
        db: Session,
        run_id: int | None,
        case_status: str | None,
    ) -> list[InvestigationCase]:

        conditions = []

        if run_id is not None:
            conditions.append(
                InvestigationCase.run_id
                == run_id,
            )

        if case_status:
            conditions.append(
                InvestigationCase.status
                == case_status,
            )

        query = select(
            InvestigationCase,
        ).order_by(
            InvestigationCase.id.desc(),
        )

        if conditions:
            query = query.where(
                *conditions,
            )

        return db.scalars(query).all()

    def get_case(
        self,
        db: Session,
        case_id: int,
    ) -> InvestigationCase:

        case = db.get(
            InvestigationCase,
            case_id,
        )

        if case is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investigation case not found",
            )

        return case

    def create_case(
        self,
        db: Session,
        match_id: int,
        user_id: int | None,
    ) -> InvestigationCase:

        match = db.get(
            ReconciliationMatch,
            match_id,
        )

        if match is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found",
            )

        if match.status == "matched":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Investigation cases can only be "
                    "created for mismatched or "
                    "unmatched records."
                ),
            )

        existing = db.scalar(
            select(InvestigationCase).where(
                InvestigationCase.match_id
                == match_id,
            )
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "An investigation case already "
                    "exists for this match."
                ),
            )

        case = InvestigationCase(
            match_id=match_id,
            run_id=match.run_id,
            status="open",
            root_cause=match.root_cause,
            created_by_id=user_id,
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        return case

    def update_case(
        self,
        db: Session,
        case_id: int,
        data: InvestigationCaseUpdate,
        user_id: int | None,
    ) -> InvestigationCase:

        case = self.get_case(db, case_id)

        if data.status is not None:

            if data.status not in ALLOWED_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid status. Allowed: "
                        + ", ".join(
                            ALLOWED_STATUSES,
                        )
                    ),
                )

            case.status = data.status

        if data.root_cause is not None:
            case.root_cause = data.root_cause

        if data.resolution_note is not None:
            case.resolution_note = (
                data.resolution_note
            )

        if data.assigned_to_id is not None:
            case.assigned_to_id = (
                data.assigned_to_id
            )

        db.commit()
        db.refresh(case)

        return case
