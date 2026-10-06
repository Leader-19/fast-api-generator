from __future__ import annotations

import os
import traceback
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.reconciliation import (
    EvidenceFile,
    ReconciliationMatch,
    ReconciliationRecord,
    ReconciliationRun,
)
from app.repositories.evidence_repository import (
    EvidenceRepository,
)
from app.repositories.reconciliation_repository import (
    ReconciliationRepository,
)
from app.schemas.reconciliation import (
    PaginatedMatchesResponse,
    MatchResponse,
    ReconciliationRunResponse,
    RunSummaryResponse,
)
from app.utils.ra_reader import (
    RaFileError,
    read_ra_file,
)


# Tolerance rules for a "matched" pair:
CHARGE_TOLERANCE = 0.01
DURATION_TOLERANCE = 0
VOLUME_TOLERANCE = 0.01


def _round2(value: float) -> float:
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        ),
    )


class ReconciliationService:

    def __init__(self):
        self.repository = ReconciliationRepository()
        self.evidence_repository = (
            EvidenceRepository()
        )

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_runs(
        self,
        db: Session,
    ) -> list[ReconciliationRunResponse]:
        runs = self.repository.get_runs(db)

        return [
            ReconciliationRunResponse.model_validate(
                run,
            )
            for run in runs
        ]

    def get_run_summary(
        self,
        db: Session,
    ) -> RunSummaryResponse:

        data = self.repository.get_run_summary(
            db,
        )

        return RunSummaryResponse(
            runs=[
                ReconciliationRunResponse.model_validate(
                    run,
                )
                for run in data["runs"]
            ],
            total_runs=data["total_runs"],
            completed_runs=data["completed_runs"],
            failed_runs=data["failed_runs"],
            total_matched=data["total_matched"],
            total_mismatched=data["total_mismatched"],
            total_unmatched=data["total_unmatched"],
            total_variance=_round2(
                data["total_variance"],
            ),
        )

    def get_run(
        self,
        db: Session,
        run_id: int,
    ) -> ReconciliationRun:

        run = self.repository.get_run(
            db,
            run_id,
        )

        if run is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reconciliation run not found",
            )

        return run

    def get_run_matches_page(
        self,
        db: Session,
        run_id: int,
        status_filter: str | None,
        page: int,
        page_size: int,
    ) -> PaginatedMatchesResponse:

        self.get_run(db, run_id)

        page = max(page, 1)
        page_size = min(max(page_size, 1), 200)

        matches, total = (
            self.repository.get_matches_page(
                db,
                run_id,
                status_filter,
                page,
                page_size,
            )
        )

        rows = (
            self.repository.get_matches_with_records(
                db,
                run_id,
            )
        )

        rows_by_match_id = {
            row["match"].id: row
            for row in rows
            if row["match"].id
            in {m.id for m in matches}
        }

        items: list[MatchResponse] = []

        for match in matches:

            row = rows_by_match_id.get(
                match.id,
            )

            record_a = (
                row["record_a"] if row else None
            )

            record_b = (
                row["record_b"] if row else None
            )

            primary = (
                record_a or record_b
            )

            items.append(
                MatchResponse(
                    id=match.id,
                    run_id=match.run_id,
                    status=match.status,
                    charge_variance=_round2(
                        match.charge_variance,
                    ),
                    duration_variance=match.duration_variance,
                    volume_variance=_round2(
                        match.volume_variance,
                    ),
                    root_cause=match.root_cause,
                    reference=(
                        primary.reference
                        if primary
                        else ""
                    ),
                    partner=(
                        primary.partner
                        if primary
                        else ""
                    ),
                    record_date=(
                        primary.record_date
                        if primary
                        else None
                    ),
                    side_a_charge=(
                        record_a.charge
                        if record_a
                        else None
                    ),
                    side_b_charge=(
                        record_b.charge
                        if record_b
                        else None
                    ),
                ),
            )

        pages = (
            (total + page_size - 1)
            // page_size
        ) or 1

        return PaginatedMatchesResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )

    def get_run_root_causes(
        self,
        db: Session,
        run_id: int,
    ) -> list[dict]:

        self.get_run(db, run_id)

        return self.repository.get_root_cause_breakdown(
            db,
            run_id,
        )

    # ------------------------------------------------------------------
    # Write: create + execute a run
    # ------------------------------------------------------------------

    def create_run(
        self,
        db: Session,
        name: str,
        file_a: UploadFile,
        file_b: UploadFile,
        user_id: int | None,
        input_directory: str | None = None,
    ) -> ReconciliationRunResponse:

        run = ReconciliationRun(
            name=name,
            status="pending",
            created_by_id=user_id,
        )

        run = self.repository.create_run(
            db,
            run,
        )

        try:
            self._execute_run(
                db,
                run,
                file_a,
                file_b,
                input_directory,
            )

        except HTTPException:

            run.status = "failed"
            run.error_message = (
                "Run validation failed."
            )
            run.completed_at = datetime.utcnow()

            self.repository.update_run(
                db,
                run,
            )

            raise

        except Exception as exc:

            print(
                "\n========== RECONCILIATION ERROR ==========",
            )
            print(repr(exc))
            traceback.print_exc()
            print(
                "==========================================\n",
            )

            db.rollback()

            run = self.repository.get_run(
                db,
                run.id,
            )

            if run is not None:

                run.status = "failed"
                run.error_message = str(exc)[:2000]
                run.completed_at = datetime.utcnow()

                self.repository.update_run(
                    db,
                    run,
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Reconciliation failed: "
                    f"{exc}"
                ),
            )

        return ReconciliationRunResponse.model_validate(
            run,
        )

    def _validate_upload(
        self,
        file: UploadFile,
        side: str,
    ) -> None:

        filename = file.filename or ""

        if not filename.lower().endswith(
            ".csv",
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"File for side {side} must be "
                    f"a CSV file."
                ),
            )

    def _save_upload(
        self,
        file: UploadFile,
        run_id: int,
        side: str,
        input_directory: str,
    ) -> tuple[str, str]:

        safe_name = os.path.basename(
            file.filename
            or f"{side}.csv",
        )

        destination = os.path.join(
            input_directory,
            f"run_{run_id}_{side}_"
            f"{safe_name}",
        )

        with open(
            destination,
            "wb",
        ) as output:

            output.write(
                file.file.read(),
            )

        return destination, safe_name

    def _execute_run(
        self,
        db: Session,
        run: ReconciliationRun,
        file_a: UploadFile,
        file_b: UploadFile,
        input_directory: str | None,
    ) -> None:

        self._validate_upload(file_a, "A")
        self._validate_upload(file_b, "B")

        base_directory = (
            input_directory
            or settings.ra_input_path
        )

        os.makedirs(
            base_directory,
            exist_ok=True,
        )

        run.status = "running"
        run.started_at = datetime.utcnow()

        self.repository.update_run(
            db,
            run,
        )

        path_a, name_a = self._save_upload(
            file_a,
            run.id,
            "A",
            base_directory,
        )

        path_b, name_b = self._save_upload(
            file_b,
            run.id,
            "B",
            base_directory,
        )

        # Save evidence rows
        for side, path, name, file in (
            (
                "A",
                path_a,
                name_a,
                file_a,
            ),
            (
                "B",
                path_b,
                name_b,
                file_b,
            ),
        ):

            self.evidence_repository.create(
                db,
                EvidenceFile(
                    run_id=run.id,
                    side=side,
                    filename=name,
                    file_path=path,
                ),
            )

        # Parse files
        try:

            records_a, warnings_a = (
                read_ra_file(path_a, "A")
            )

            records_b, warnings_b = (
                read_ra_file(path_b, "B")
            )

        except RaFileError as exc:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )

        if not records_a and not records_b:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Both input files contain "
                    "no usable records."
                ),
            )

        # Persist records
        records: list[ReconciliationRecord] = []

        for data in records_a + records_b:

            records.append(
                ReconciliationRecord(
                    run_id=run.id,
                    side=data["side"],
                    reference=data["reference"],
                    partner=data["partner"],
                    record_date=data["record_date"],
                    duration_seconds=data[
                        "duration_seconds"
                    ],
                    volume_kb=data["volume_kb"],
                    charge=data["charge"],
                    row_number=data["row_number"],
                ),
            )

        db.add_all(records)

        db.flush()

        warnings = warnings_a + warnings_b

        if warnings:
            run.error_message = (
                "Parsed with warnings: "
                + " | ".join(warnings[:20])
            )

        # Execute matching
        self._match_records(
            db,
            run,
            records_a,
            records_b,
        )

        run.status = "completed"
        run.completed_at = datetime.utcnow()

        self.repository.update_run(
            db,
            run,
        )

    # ------------------------------------------------------------------
    # Matching engine
    # ------------------------------------------------------------------

    def _match_records(
        self,
        db: Session,
        run: ReconciliationRun,
        records_a: list[dict],
        records_b: list[dict],
    ) -> None:

        by_reference_b: dict[str, list[dict]] = {}

        for record in records_b:
            by_reference_b.setdefault(
                record["reference"],
                [],
            ).append(record)

        matches: list[ReconciliationMatch] = []

        used_b_ids: set[int] = set()

        matched = 0
        mismatched = 0
        unmatched = 0
        total_variance = 0.0

        from app.services.root_cause_service import (
            classify_root_cause,
        )

        for record_a in records_a:

            candidates = by_reference_b.get(
                record_a["reference"],
                [],
            )

            record_b = next(
                (
                    candidate
                    for candidate in candidates
                    if id(candidate)
                    not in used_b_ids
                ),
                None,
            )

            if record_b is None:

                matches.append(
                    ReconciliationMatch(
                        run_id=run.id,
                        record_a_id=None,
                        record_b_id=None,
                        status="unmatched",
                        root_cause=(
                            "missing_on_side_b"
                        ),
                    ),
                )

                unmatched += 1

                continue

            used_b_ids.add(
                id(record_b),
            )

            charge_variance = _round2(
                record_a["charge"]
                - record_b["charge"],
            )

            duration_variance = (
                record_a["duration_seconds"]
                - record_b["duration_seconds"]
            )

            volume_variance = _round2(
                record_a["volume_kb"]
                - record_b["volume_kb"],
            )

            is_matched = (
                abs(charge_variance)
                <= CHARGE_TOLERANCE
                and abs(duration_variance)
                <= DURATION_TOLERANCE
                and abs(volume_variance)
                <= VOLUME_TOLERANCE
            )

            if is_matched:

                match_status = "matched"
                matched += 1

                root_cause = None

            else:

                match_status = "mismatched"
                mismatched += 1

                total_variance += abs(
                    charge_variance,
                )

                root_cause = classify_root_cause(
                    charge_variance=charge_variance,
                    duration_variance=duration_variance,
                    volume_variance=volume_variance,
                    date_a=record_a["record_date"],
                    date_b=record_b["record_date"],
                    partner_a=record_a["partner"],
                    partner_b=record_b["partner"],
                )

            record_ids = self._record_ids(
                db,
                run.id,
                record_a,
                record_b,
            )

            matches.append(
                ReconciliationMatch(
                    run_id=run.id,
                    record_a_id=record_ids[
                        "record_a_id"
                    ],
                    record_b_id=record_ids[
                        "record_b_id"
                    ],
                    status=match_status,
                    charge_variance=charge_variance,
                    duration_variance=duration_variance,
                    volume_variance=volume_variance,
                    root_cause=root_cause,
                ),
            )

        # Side B records with no side A pair
        for record_b in records_b:

            if (
                id(record_b)
                in used_b_ids
            ):
                continue

            matches.append(
                ReconciliationMatch(
                    run_id=run.id,
                    record_a_id=None,
                    record_b_id=None,
                    status="unmatched",
                    root_cause=(
                        "missing_on_side_a"
                    ),
                ),
            )

            unmatched += 1

        self.repository.create_matches(
            db,
            matches,
        )

        run.total_records = (
            len(records_a) + len(records_b)
        )

        run.matched_records = matched
        run.mismatched_records = mismatched
        run.unmatched_records = unmatched
        run.total_variance = _round2(
            total_variance,
        )

    def _record_ids(
        self,
        db: Session,
        run_id: int,
        record_a: dict,
        record_b: dict,
    ) -> dict:

        # Records were flushed in insertion
        # order, so resolve ids by a fresh
        # lookup each execution (no caching,
        # so reprocessing a run in the same
        # session stays correct).
        from sqlalchemy import select

        rows = db.scalars(
            select(ReconciliationRecord)
            .where(
                ReconciliationRecord.run_id
                == run_id,
            )
        ).all()

        record_id_map = {
            (
                row.side,
                row.reference,
                row.row_number,
            ): row.id
            for row in rows
        }

        key_a = (
            "A",
            record_a["reference"],
            record_a["row_number"],
        )

        key_b = (
            "B",
            record_b["reference"],
            record_b["row_number"],
        )

        return {
            "record_a_id": (
                record_id_map.get(key_a)
            ),
            "record_b_id": (
                record_id_map.get(key_b)
            ),
        }

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_run(
        self,
        db: Session,
        run_id: int,
    ) -> None:

        run = self.get_run(db, run_id)

        # Remove stored evidence files
        for evidence in (
            self.evidence_repository.get_by_run(
                db,
                run_id,
            )
        ):

            try:
                if os.path.exists(
                    evidence.file_path,
                ):
                    os.remove(
                        evidence.file_path,
                    )

            except OSError:

                pass

        self.repository.delete_run(
            db,
            run,
        )
