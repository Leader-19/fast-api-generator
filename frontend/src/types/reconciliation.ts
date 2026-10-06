export type RunStatus =
    | 'pending'
    | 'running'
    | 'completed'
    | 'failed'

export type MatchStatus =
    | 'matched'
    | 'mismatched'
    | 'unmatched'

export type CaseStatus =
    | 'open'
    | 'in_progress'
    | 'resolved'
    | 'closed'

export interface ReconciliationRun {
    id: number
    name: string
    status: RunStatus
    total_records: number
    matched_records: number
    mismatched_records: number
    unmatched_records: number
    total_variance: number
    error_message: string | null
    started_at: string | null
    completed_at: string | null
    created_at: string
    created_by_id: number | null
}

export interface RunSummary {
    runs: ReconciliationRun[]
    total_runs: number
    completed_runs: number
    failed_runs: number
    total_matched: number
    total_mismatched: number
    total_unmatched: number
    total_variance: number
}

export interface Match {
    id: number
    run_id: number
    status: MatchStatus
    charge_variance: number
    duration_variance: number
    volume_variance: number
    root_cause: string | null
    reference: string
    partner: string
    record_date: string | null
    side_a_charge: number | null
    side_b_charge: number | null
}

export interface PaginatedMatches {
    items: Match[]
    total: number
    page: number
    page_size: number
    pages: number
}

export interface RootCauseBreakdownItem {
    root_cause: string
    count: number
    total_variance: number
}

export interface InvestigationCase {
    id: number
    match_id: number
    run_id: number
    status: CaseStatus
    root_cause: string | null
    resolution_note: string | null
    assigned_to_id: number | null
    created_by_id: number | null
    created_at: string
    updated_at: string
}

export interface InvestigationCaseUpdate {
    status?: CaseStatus
    root_cause?: string | null
    resolution_note?: string | null
    assigned_to_id?: number | null
}
