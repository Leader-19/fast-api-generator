<template>
    <div>
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div class="flex items-center gap-3">
                <button type="button" @click="router.back()"
                    class="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                </button>
                <div>
                    <h2 class="text-2xl font-bold text-slate-800">{{ run?.name ?? `Run #${runId}` }}</h2>
                    <p class="text-sm text-slate-500 mt-1" v-if="run">
                        {{ run.total_records }} records ·
                        <span class="text-emerald-600">{{ run.matched_records }} matched</span> ·
                        <span class="text-amber-600">{{ run.mismatched_records }} mismatched</span> ·
                        <span class="text-red-600">{{ run.unmatched_records }} unmatched</span>
                        · variance {{ formatAmount(run.total_variance) }}
                    </p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span v-if="run" class="px-2.5 py-1 text-xs rounded-full font-medium" :class="statusClass(run.status)">
                    {{ run.status }}
                </span>
                <button type="button" @click="handleExport" :disabled="exporting"
                    class="inline-flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-200 hover:border-green-300 hover:bg-green-50 text-slate-700 text-sm font-medium rounded-lg transition disabled:opacity-50">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5 5-5M12 15V3" />
                    </svg>
                    {{ exporting ? 'Exporting...' : 'Export Excel' }}
                </button>
            </div>
        </div>

        <!-- Error / Success -->
        <UiAlert v-if="error" variant="error" dismissible @dismiss="error = ''">{{ error }}</UiAlert>
        <UiAlert v-if="successMessage" variant="success" dismissible @dismiss="successMessage = ''">
            {{ successMessage }}
        </UiAlert>

        <!-- Root causes panel -->
        <div v-if="rootCauses.length > 0" class="mb-6 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
            <div v-for="item in rootCauses" :key="item.root_cause"
                class="bg-white border border-slate-200 rounded-xl p-3 shadow-sm">
                <p class="text-xs font-medium text-slate-500 truncate" :title="rootCauseLabel(item.root_cause)">
                    {{ rootCauseLabel(item.root_cause) }}
                </p>
                <div class="flex items-baseline justify-between mt-1">
                    <p class="text-lg font-bold text-slate-800">{{ item.count }}</p>
                    <p class="text-xs text-amber-600 font-medium">{{ formatAmount(item.total_variance) }}</p>
                </div>
            </div>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap items-center gap-2 mb-4">
            <button v-for="option in filterOptions" :key="option.value" type="button" @click="setFilter(option.value)"
                class="px-3 py-1.5 text-sm rounded-lg border transition"
                :class="statusFilter === option.value
                    ? 'bg-blue-600 border-blue-600 text-white'
                    : 'bg-white border-slate-200 text-slate-600 hover:border-blue-300 hover:bg-blue-50'">
                {{ option.label }}
                <span v-if="option.count !== null"
                    class="ml-1 px-1.5 py-0.5 text-xs rounded-full"
                    :class="statusFilter === option.value ? 'bg-white/20' : 'bg-slate-100'">
                    {{ option.count }}
                </span>
            </button>
        </div>

        <!-- Matches table -->
        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead class="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Reference</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Partner</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Date</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Side A</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Side B</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Variance</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Status</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Root cause</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-if="loading">
                            <td colspan="9" class="px-2 py-2">
                                <UiSkeletonTable :rows="6" :cols="9" />
                            </td>
                        </tr>
                        <tr v-else-if="matches && matches.items.length === 0">
                            <td colspan="9" class="px-4 py-8 text-center text-slate-400">
                                No matches found for this filter.
                            </td>
                        </tr>
                        <tr v-for="match in matches?.items ?? []" :key="match.id" class="hover:bg-slate-50 transition">
                            <td class="px-4 py-3 font-medium text-slate-800">{{ match.reference }}</td>
                            <td class="px-4 py-3 text-slate-600">{{ match.partner || '—' }}</td>
                            <td class="px-4 py-3 text-slate-500 text-xs">{{ formatDateTime(match.record_date) }}</td>
                            <td class="px-4 py-3 text-right text-slate-700">{{ formatAmount(match.side_a_charge) }}</td>
                            <td class="px-4 py-3 text-right text-slate-700">{{ formatAmount(match.side_b_charge) }}</td>
                            <td class="px-4 py-3 text-right font-medium"
                                :class="match.charge_variance === 0 ? 'text-slate-500' : (match.charge_variance > 0 ? 'text-emerald-600' : 'text-red-600')">
                                {{ formatAmount(match.charge_variance) }}
                            </td>
                            <td class="px-4 py-3">
                                <UiBadge :variant="matchStatusVariant(match.status)">{{ match.status }}</UiBadge>
                            </td>
                            <td class="px-4 py-3 text-xs text-slate-500">
                                {{ match.root_cause ? rootCauseLabel(match.root_cause) : '—' }}
                            </td>
                            <td class="px-4 py-3 text-right">
                                <button v-if="match.status !== 'matched'" type="button"
                                    @click="handleCreateCase(match)"
                                    :disabled="creatingCaseId === match.id"
                                    class="px-2.5 py-1 text-xs font-medium rounded-lg border transition disabled:opacity-50"
                                    :class="caseMatchIds.has(match.id)
                                        ? 'bg-slate-50 text-slate-400 border-slate-200 cursor-default'
                                        : 'bg-white text-blue-600 border-blue-200 hover:bg-blue-50'">
                                    {{ caseMatchIds.has(match.id) ? 'Case exists' : 'Investigate' }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div v-if="matches && matches.pages > 1"
                class="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-slate-50">
                <p class="text-xs text-slate-500">
                    Page {{ matches.page }} of {{ matches.pages }} · {{ matches.total }} items
                </p>
                <div class="flex gap-2">
                    <button type="button" :disabled="matches.page <= 1" @click="changePage(matches.page - 1)"
                        class="px-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40 transition">
                        Previous
                    </button>
                    <button type="button" :disabled="matches.page >= matches.pages"
                        @click="changePage(matches.page + 1)"
                        class="px-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40 transition">
                        Next
                    </button>
                </div>
            </div>
        </div>

        <!-- Case created modal -->
        <UiModal :open="showCaseModal" title="Investigation Case Created"
            :subtitle="`Case #${createdCase?.id} was created for match ${createdCase?.match_id} (${createdCase?.root_cause ? rootCauseLabel(createdCase.root_cause) : 'unclassified'}). Manage it in the Investigations board.`"
            max-width="md" @close="showCaseModal = false">
            <div class="flex justify-end">
                <button type="button" @click="showCaseModal = false"
                    class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
                    OK
                </button>
            </div>
        </UiModal>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
    getRun,
    getMatches,
    getRootCauses,
    getCases,
    createCase,
    exportRunExcel,
    downloadBlob,
    formatAmount,
    formatDateTime,
    getErrorMessage,
} from '@/services/reconciliation'
import type {
    Match,
    MatchStatus,
    PaginatedMatches,
    ReconciliationRun,
    RootCauseBreakdownItem,
    InvestigationCase,
} from '@/types/reconciliation'
import { UiBadge, UiModal, UiSkeletonTable, UiAlert } from '@/components/ui'

const route = useRoute()
const router = useRouter()

const runId = computed(() => Number(route.params.runId))

const run = ref<ReconciliationRun | null>(null)
const matches = ref<PaginatedMatches | null>(null)
const rootCauses = ref<RootCauseBreakdownItem[]>([])
const cases = ref<InvestigationCase[]>([])

const loading = ref(false)
const exporting = ref(false)
const creatingCaseId = ref<number | null>(null)
const error = ref('')
const successMessage = ref('')

const statusFilter = ref<MatchStatus | ''>('')
const page = ref(1)
const pageSize = 20

const showCaseModal = ref(false)
const createdCase = ref<InvestigationCase | null>(null)

const caseMatchIds = computed(
    () => new Set(cases.value.map((c) => c.match_id)),
)

const filterOptions = computed<{ value: MatchStatus | ''; label: string; count: number | null }[]>(() => [
    { value: '', label: 'All', count: matches.value ? matches.value.total : null },
    { value: 'matched', label: 'Matched', count: run.value?.matched_records ?? null },
    { value: 'mismatched', label: 'Mismatched', count: run.value?.mismatched_records ?? null },
    { value: 'unmatched', label: 'Unmatched', count: run.value?.unmatched_records ?? null },
])

const statusClass = (status: string): string => {
    switch (status) {
        case 'completed':
            return 'bg-green-50 text-green-700'
        case 'failed':
            return 'bg-red-50 text-red-700'
        case 'running':
            return 'bg-amber-50 text-amber-700'
        default:
            return 'bg-slate-100 text-slate-500'
    }
}

const matchStatusVariant = (status: string) =>
    status === 'matched'
        ? 'success'
        : status === 'mismatched'
          ? 'warning'
          : 'danger'

const ROOT_CAUSE_LABELS: Record<string, string> = {
    rate_mismatch: 'Rate mismatch',
    usage_mismatch: 'Usage mismatch',
    partner_mismatch: 'Partner mismatch',
    date_mismatch: 'Date mismatch',
    undercharge_side_a: 'Undercharge (side A)',
    overcharge_side_a: 'Overcharge (side A)',
    missing_on_side_a: 'Missing on side A',
    missing_on_side_b: 'Missing on side B',
    unclassified: 'Unclassified',
}

const rootCauseLabel = (key: string): string =>
    ROOT_CAUSE_LABELS[key] ?? key

const loadRun = async (): Promise<void> => {
    error.value = ''
    try {
        run.value = await getRun(runId.value)
    } catch (err) {
        error.value = await getErrorMessage(err)
    }
}

const loadMatches = async (): Promise<void> => {
    loading.value = true
    error.value = ''
    try {
        matches.value = await getMatches(runId.value, {
            status: statusFilter.value || undefined,
            page: page.value,
            page_size: pageSize,
        })
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        loading.value = false
    }
}

const loadRootCauses = async (): Promise<void> => {
    try {
        rootCauses.value = await getRootCauses(runId.value)
    } catch {
        rootCauses.value = []
    }
}

const loadCases = async (): Promise<void> => {
    try {
        cases.value = await getCases({ run_id: runId.value })
    } catch {
        cases.value = []
    }
}

const setFilter = (value: MatchStatus | ''): void => {
    statusFilter.value = value
    page.value = 1
}

const changePage = (newPage: number): void => {
    page.value = newPage
}

watch(statusFilter, loadMatches)
watch(page, loadMatches)

const handleCreateCase = async (match: Match): Promise<void> => {
    creatingCaseId.value = match.id
    error.value = ''
    try {
        createdCase.value = await createCase(match.id)
        showCaseModal.value = true
        await loadCases()
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        creatingCaseId.value = null
    }
}

const handleExport = async (): Promise<void> => {
    exporting.value = true
    error.value = ''
    try {
        const blob = await exportRunExcel(runId.value)
        downloadBlob(blob, `reconciliation_run_${runId.value}.xlsx`)
        successMessage.value = 'Excel report downloaded.'
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        exporting.value = false
    }
}

onMounted(async () => {
    await Promise.all([loadRun(), loadMatches(), loadRootCauses(), loadCases()])
})
</script>
