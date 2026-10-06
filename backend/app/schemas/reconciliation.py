from datetime import datetime

from pydantic import BaseModel, Field


class ReconciliationRunCreate(BaseModel):
    name: str
    description: str | None = None


class ReconciliationRunResponse(BaseModel):
    id: int
    name: str
    status: str
    total_records: int
    matched_records: int
    mismatched_records: int
    unmatched_records: int
    total_variance: float
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    created_by_id: int | None

    model_config = {
        "from_attributes": True,
    }


class RunSummaryResponse(BaseModel):
    runs: list[ReconciliationRunResponse] = Field(
        default_factory=list,
    )

    total_runs: int = 0

    completed_runs: int = 0

    failed_runs: int = 0

    total_matched: int = 0

    total_mismatched: int = 0

    total_unmatched: int = 0

    total_variance: float = 0.0


class EvidenceFileResponse(BaseModel):
    id: int
    run_id: int
    side: str
    filename: str
    row_count: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class MatchResponse(BaseModel):
    id: int
    run_id: int
    status: str
    charge_variance: float
    duration_variance: int
    volume_variance: float
    root_cause: str | None

    reference: str
    partner: str
    record_date: datetime | None

    side_a_charge: float | None = None
    side_b_charge: float | None = None

    model_config = {
        "from_attributes": True,
    }


class PaginatedMatchesResponse(BaseModel):
    items: list[MatchResponse] = Field(
        default_factory=list,
    )

    total: int = 0

    page: int = 1

    page_size: int = 50

    pages: int = 1


class InvestigationCaseCreate(BaseModel):
    match_id: int


class InvestigationCaseUpdate(BaseModel):
    status: str | None = None
    root_cause: str | None = None
    resolution_note: str | None = None
    assigned_to_id: int | None = None


class InvestigationCaseResponse(BaseModel):
    id: int
    match_id: int
    run_id: int
    status: str
    root_cause: str | None
    resolution_note: str | None
    assigned_to_id: int | None
    created_by_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class RootCauseBreakdownItem(BaseModel):
    root_cause: str
    count: int
    total_variance: float


class RootCauseBreakdownResponse(BaseModel):
    items: list[RootCauseBreakdownItem] = Field(
        default_factory=list,
    )
