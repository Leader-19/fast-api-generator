from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reconciliation import EvidenceFile


class EvidenceRepository:

    def create(
        self,
        db: Session,
        evidence: EvidenceFile,
    ) -> EvidenceFile:
        db.add(evidence)
        db.commit()
        db.refresh(evidence)

        return evidence

    def get_by_run(
        self,
        db: Session,
        run_id: int,
    ) -> list[EvidenceFile]:
        return db.scalars(
            select(EvidenceFile)
            .where(
                EvidenceFile.run_id == run_id,
            )
            .order_by(
                EvidenceFile.id.asc(),
            )
        ).all()

    def get_by_run_and_side(
        self,
        db: Session,
        run_id: int,
        side: str,
    ) -> EvidenceFile | None:
        return db.scalar(
            select(EvidenceFile).where(
                EvidenceFile.run_id == run_id,
                EvidenceFile.side == side,
            )
        )
