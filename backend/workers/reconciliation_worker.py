"""
Standalone reconciliation worker.

Processes runs left in `pending` or
`running` state (e.g. after a crash, or
queued by another process).

Usage:
    python -m workers.reconciliation_worker
"""

from __future__ import annotations

import os
import sys
import time
import traceback
from datetime import datetime

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__),
        ),
    ),
)

from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.reconciliation import (
    EvidenceFile,
    ReconciliationMatch,
    ReconciliationRecord,
    ReconciliationRun,
)
from app.services.reconciliation_service import (
    ReconciliationService,
)
from app.utils.ra_reader import read_ra_file


POLL_INTERVAL_SECONDS = 5

CLAIMED_STATUSES = ("pending", "running")


def claim_next_run(
    db,
) -> ReconciliationRun | None:

    run = db.scalars(
        select(ReconciliationRun)
        .where(
            ReconciliationRun.status.in_(
                CLAIMED_STATUSES,
            ),
        )
        .order_by(
            ReconciliationRun.id.asc(),
        )
        .limit(1),
    ).first()

    return run


def process_run(
    db,
    run: ReconciliationRun,
    service: ReconciliationService,
) -> None:

    evidence_a = db.scalar(
        select(EvidenceFile).where(
            EvidenceFile.run_id == run.id,
            EvidenceFile.side == "A",
        ),
    )

    evidence_b = db.scalar(
        select(EvidenceFile).where(
            EvidenceFile.run_id == run.id,
            EvidenceFile.side == "B",
        ),
    )

    if evidence_a is None or evidence_b is None:
        raise RuntimeError(
            f"Run {run.id} is missing evidence "
            f"files; cannot process."
        )

    # Fresh state
    db.query(ReconciliationMatch).filter(
        ReconciliationMatch.run_id == run.id,
    ).delete()

    db.query(ReconciliationRecord).filter(
        ReconciliationRecord.run_id == run.id,
    ).delete()

    db.commit()

    records_a, warnings_a = read_ra_file(
        evidence_a.file_path,
        "A",
    )

    records_b, warnings_b = read_ra_file(
        evidence_b.file_path,
        "B",
    )

    run.status = "running"
    run.started_at = datetime.utcnow()
    db.commit()

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

    service._match_records(
        db,
        run,
        records_a,
        records_b,
    )

    run.status = "completed"
    run.completed_at = datetime.utcnow()

    db.commit()


def main() -> None:

    service = ReconciliationService()

    print(
        "Reconciliation worker started. "
        "Polling every "
        f"{POLL_INTERVAL_SECONDS}s. "
        "Ctrl+C to stop.",
    )

    while True:

        db = SessionLocal()

        try:

            run = claim_next_run(db)

            if run is None:
                time.sleep(
                    POLL_INTERVAL_SECONDS,
                )
                continue

            print(
                f"[RUN {run.id}] Processing "
                f"'{run.name}'...",
            )

            try:

                process_run(db, run, service)

                print(
                    f"[RUN {run.id}] Completed: "
                    f"matched={run.matched_records} "
                    f"mismatched={run.mismatched_records} "
                    f"unmatched={run.unmatched_records}",
                )

            except Exception as exc:

                db.rollback()

                print(
                    f"[RUN {run.id}] FAILED: "
                    f"{exc}",
                )

                traceback.print_exc()

                run = db.get(
                    ReconciliationRun,
                    run.id,
                )

                if run is not None:

                    run.status = "failed"
                    run.error_message = (
                        str(exc)[:2000]
                    )
                    run.completed_at = (
                        datetime.utcnow()
                    )

                    db.commit()

        finally:

            db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nWorker stopped.")
