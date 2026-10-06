from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reconciliation import (
    ReconciliationMatch,
    ReconciliationRecord,
    ReconciliationRun,
)


class ReconciliationRepository:

    # ------------------------------------------------------------------
    # Runs
    # ------------------------------------------------------------------

    def create_run(
        self,
        db: Session,
        run: ReconciliationRun,
    ) -> ReconciliationRun:
        db.add(run)
        db.commit()
        db.refresh(run)

        return run

    def get_runs(
        self,
        db: Session,
    ) -> list[ReconciliationRun]:
        return db.scalars(
            select(ReconciliationRun).order_by(
                ReconciliationRun.id.desc(),
            )
        ).all()

    def get_run(
        self,
        db: Session,
        run_id: int,
    ) -> ReconciliationRun | None:
        return db.get(ReconciliationRun, run_id)

    def get_latest_completed_run(
        self,
        db: Session,
    ) -> ReconciliationRun | None:
        return db.scalar(
            select(ReconciliationRun)
            .where(
                ReconciliationRun.status
                == "completed",
            )
            .order_by(
                ReconciliationRun.id.desc(),
            )
        )

    def update_run(
        self,
        db: Session,
        run: ReconciliationRun,
    ) -> ReconciliationRun:
        db.commit()
        db.refresh(run)

        return run

    def delete_run(
        self,
        db: Session,
        run: ReconciliationRun,
    ) -> None:
        db.delete(run)
        db.commit()

    def get_run_summary(
        self,
        db: Session,
    ) -> dict:
        runs = self.get_runs(db)

        completed = [
            run
            for run in runs
            if run.status == "completed"
        ]

        failed = [
            run
            for run in runs
            if run.status == "failed"
        ]

        return {
            "runs": runs,
            "total_runs": len(runs),
            "completed_runs": len(completed),
            "failed_runs": len(failed),
            "total_matched": sum(
                run.matched_records
                for run in completed
            ),
            "total_mismatched": sum(
                run.mismatched_records
                for run in completed
            ),
            "total_unmatched": sum(
                run.unmatched_records
                for run in completed
            ),
            "total_variance": sum(
                run.total_variance
                for run in completed
            ),
        }

    # ------------------------------------------------------------------
    # Matches
    # ------------------------------------------------------------------

    def create_matches(
        self,
        db: Session,
        matches: list[ReconciliationMatch],
    ) -> None:
        db.add_all(matches)
        db.commit()

    def get_matches_page(
        self,
        db: Session,
        run_id: int,
        status_filter: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ReconciliationMatch], int]:

        conditions = [
            ReconciliationMatch.run_id == run_id,
        ]

        if status_filter:
            conditions.append(
                ReconciliationMatch.status
                == status_filter,
            )

        total = db.scalar(
            select(func.count()).select_from(
                ReconciliationMatch
            ).where(*conditions)
        ) or 0

        matches = db.scalars(
            select(ReconciliationMatch)
            .where(*conditions)
            .order_by(
                ReconciliationMatch.id.asc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).all()

        return matches, int(total)

    def get_matches_with_records(
        self,
        db: Session,
        run_id: int,
    ) -> list[dict]:

        record_a = ReconciliationRecord
        record_b = ReconciliationRecord

        alias_a = select(record_a).where(
            record_a.id
            == ReconciliationMatch.record_a_id,
        ).scalar_subquery()

        alias_b = select(record_b).where(
            record_b.id
            == ReconciliationMatch.record_b_id,
        ).scalar_subquery()

        matches = db.scalars(
            select(ReconciliationMatch).where(
                ReconciliationMatch.run_id
                == run_id,
            )
        ).all()

        record_ids: set[int] = set()

        for match in matches:
            if match.record_a_id:
                record_ids.add(
                    match.record_a_id,
                )

            if match.record_b_id:
                record_ids.add(
                    match.record_b_id,
                )

        records_by_id: dict[int, ReconciliationRecord] = {}

        if record_ids:
            records = db.scalars(
                select(ReconciliationRecord).where(
                    ReconciliationRecord.id.in_(
                        record_ids,
                    ),
                )
            ).all()

            records_by_id = {
                record.id: record
                for record in records
            }

        rows: list[dict] = []

        for match in matches:
            record_a_row = (
                records_by_id.get(
                    match.record_a_id,
                )
                if match.record_a_id
                else None
            )

            record_b_row = (
                records_by_id.get(
                    match.record_b_id,
                )
                if match.record_b_id
                else None
            )

            primary = (
                record_a_row
                or record_b_row
            )

            rows.append(
                {
                    "match": match,
                    "record_a": record_a_row,
                    "record_b": record_b_row,
                    "primary": primary,
                },
            )

        return rows

    def get_root_cause_breakdown(
        self,
        db: Session,
        run_id: int,
    ) -> list[dict]:

        rows = db.execute(
            select(
                ReconciliationMatch.root_cause,
                func.count().label("count"),
                func.coalesce(
                    func.sum(
                        func.abs(
                            ReconciliationMatch.charge_variance,
                        ),
                    ),
                    0.0,
                ).label("total_variance"),
            )
            .where(
                ReconciliationMatch.run_id
                == run_id,
                ReconciliationMatch.status
                != "matched",
                ReconciliationMatch.root_cause
                .isnot(None),
            )
            .group_by(
                ReconciliationMatch.root_cause,
            )
            .order_by(
                func.count().desc(),
            )
        ).all()

        return [
            {
                "root_cause": row.root_cause,
                "count": int(row.count),
                "total_variance": float(
                    row.total_variance,
                ),
            }
            for row in rows
        ]

    def count_matches_by_status(
        self,
        db: Session,
        run_id: int,
    ) -> dict[str, int]:

        rows = db.execute(
            select(
                ReconciliationMatch.status,
                func.count().label("count"),
            )
            .where(
                ReconciliationMatch.run_id
                == run_id,
            )
            .group_by(
                ReconciliationMatch.status,
            )
        ).all()

        return {
            row.status: int(row.count)
            for row in rows
        }

    def touch_run_timestamps(
        self,
        run: ReconciliationRun,
        started: bool,
    ) -> None:

        now = datetime.utcnow()

        if started:
            run.started_at = now
        else:
            run.completed_at = now
