from datetime import datetime

from sqlalchemy import DateTime, Double, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ReconciliationRun(Base):
    __tablename__ = "reconciliation_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # pending | running | completed | failed
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )

    total_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    matched_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    mismatched_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    unmatched_records: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_variance: Mapped[float] = mapped_column(
        Double,
        default=0.0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_by = relationship(
        "User",
    )

    records = relationship(
        "ReconciliationRecord",
        back_populates="run",
        cascade="all, delete-orphan",
    )

    matches = relationship(
        "ReconciliationMatch",
        back_populates="run",
        cascade="all, delete-orphan",
    )

    evidence_files = relationship(
        "EvidenceFile",
        back_populates="run",
        cascade="all, delete-orphan",
    )


class EvidenceFile(Base):
    __tablename__ = "evidence_files"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("reconciliation_runs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # A (internal records) | B (partner statement)
    side: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    run = relationship(
        "ReconciliationRun",
        back_populates="evidence_files",
    )


class ReconciliationRecord(Base):
    __tablename__ = "reconciliation_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("reconciliation_runs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    side: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    reference: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    partner: Mapped[str] = mapped_column(
        String(100),
        default="",
        nullable=False,
    )

    record_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    volume_kb: Mapped[float] = mapped_column(
        Double,
        default=0.0,
        nullable=False,
    )

    charge: Mapped[float] = mapped_column(
        Double,
        default=0.0,
        nullable=False,
    )

    row_number: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    run = relationship(
        "ReconciliationRun",
        back_populates="records",
    )


class ReconciliationMatch(Base):
    __tablename__ = "reconciliation_matches"

    id: Mapped[int] = mapped_column(primary_key=True)

    run_id: Mapped[int] = mapped_column(
        ForeignKey("reconciliation_runs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Side A record (may be NULL when the record only exists on side B)
    record_a_id: Mapped[int | None] = mapped_column(
        ForeignKey("reconciliation_records.id", ondelete="CASCADE"),
        nullable=True,
    )

    # Side B record (may be NULL when the record only exists on side A)
    record_b_id: Mapped[int | None] = mapped_column(
        ForeignKey("reconciliation_records.id", ondelete="CASCADE"),
        nullable=True,
    )

    # matched | mismatched | unmatched
    status: Mapped[str] = mapped_column(
        String(20),
        default="unmatched",
        nullable=False,
    )

    charge_variance: Mapped[float] = mapped_column(
        Double,
        default=0.0,
        nullable=False,
    )

    duration_variance: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    volume_variance: Mapped[float] = mapped_column(
        Double,
        default=0.0,
        nullable=False,
    )

    root_cause: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    run = relationship(
        "ReconciliationRun",
        back_populates="matches",
    )

    record_a = relationship(
        "ReconciliationRecord",
        foreign_keys=[record_a_id],
    )

    record_b = relationship(
        "ReconciliationRecord",
        foreign_keys=[record_b_id],
    )

    investigation_case = relationship(
        "InvestigationCase",
        back_populates="match",
        uselist=False,
    )


class InvestigationCase(Base):
    __tablename__ = "investigation_cases"

    id: Mapped[int] = mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(
        ForeignKey("reconciliation_matches.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    run_id: Mapped[int] = mapped_column(
        ForeignKey("reconciliation_runs.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # open | in_progress | resolved | closed
    status: Mapped[str] = mapped_column(
        String(20),
        default="open",
        nullable=False,
    )

    root_cause: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    resolution_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    match = relationship(
        "ReconciliationMatch",
        back_populates="investigation_case",
    )

    assigned_to = relationship(
        "User",
        foreign_keys=[assigned_to_id],
    )
