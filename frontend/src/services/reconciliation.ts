import api from './api'
import { getErrorMessage } from './pdfConverter'
import type {
    InvestigationCase,
    InvestigationCaseUpdate,
    MatchStatus,
    PaginatedMatches,
    RootCauseBreakdownItem,
    ReconciliationRun,
    RunSummary,
} from '@/types/reconciliation'

// --------------------------------------------------------------
// Runs
// --------------------------------------------------------------

export const getRunSummary = async (): Promise<RunSummary> => {
    const { data } = await api.get<RunSummary>('reconciliation/runs')
    return data
}

export const getRun = async (runId: number): Promise<ReconciliationRun> => {
    const { data } = await api.get<ReconciliationRun>(`reconciliation/runs/${runId}`)
    return data
}

export const createRun = async (
    name: string,
    fileA: File,
    fileB: File,
): Promise<ReconciliationRun> => {
    const formData = new FormData()

    formData.append('file_a', fileA)
    formData.append('file_b', fileB)

    const { data } = await api.post<ReconciliationRun>(
        `reconciliation/runs?name=${encodeURIComponent(name)}`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        },
    )

    return data
}

export const deleteRun = async (runId: number): Promise<void> => {
    await api.delete(`reconciliation/runs/${runId}`)
}

// --------------------------------------------------------------
// Matches
// --------------------------------------------------------------

export const getMatches = async (
    runId: number,
    params: {
        status?: MatchStatus
        page?: number
        page_size?: number
    } = {},
): Promise<PaginatedMatches> => {
    const { data } = await api.get<PaginatedMatches>(
        `reconciliation/runs/${runId}/matches`,
        { params },
    )
    return data
}

export const getRootCauses = async (
    runId: number,
): Promise<RootCauseBreakdownItem[]> => {
    const { data } = await api.get<RootCauseBreakdownItem[]>(
        `reconciliation/runs/${runId}/root-causes`,
    )
    return data
}

// --------------------------------------------------------------
// Investigation cases
// --------------------------------------------------------------

export const getCases = async (
    params: {
        run_id?: number
        case_status?: string
    } = {},
): Promise<InvestigationCase[]> => {
    const { data } = await api.get<InvestigationCase[]>('investigations', {
        params,
    })
    return data
}

export const createCase = async (matchId: number): Promise<InvestigationCase> => {
    const { data } = await api.post<InvestigationCase>('investigations', null, {
        params: { match_id: matchId },
    })
    return data
}

export const updateCase = async (
    caseId: number,
    payload: InvestigationCaseUpdate,
): Promise<InvestigationCase> => {
    const { data } = await api.put<InvestigationCase>(
        `investigations/${caseId}`,
        payload,
    )
    return data
}

// --------------------------------------------------------------
// Excel exports
// --------------------------------------------------------------

export const exportRunExcel = async (runId: number): Promise<Blob> => {
    const response = await api.get(
        `reports/reconciliation/runs/${runId}/excel`,
        { responseType: 'blob' },
    )
    return response.data
}

export const exportSummaryExcel = async (): Promise<Blob> => {
    const response = await api.get(
        'reports/reconciliation/summary/excel',
        { responseType: 'blob' },
    )
    return response.data
}

// --------------------------------------------------------------
// Helpers
// --------------------------------------------------------------

export { getErrorMessage }

export const downloadBlob = (blob: Blob, filename: string): void => {
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')

    link.href = url
    link.download = filename

    document.body.appendChild(link)

    link.click()

    link.remove()

    window.URL.revokeObjectURL(url)
}

export const formatDateTime = (value: string | null): string => {
    if (!value) {
        return '—'
    }

    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {
        return value
    }

    return date.toLocaleString(undefined, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    })
}

export const formatAmount = (value: number | null): string => {
    if (value === null) {
        return '—'
    }

    return value.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })
}
