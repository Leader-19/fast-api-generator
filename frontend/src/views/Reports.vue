<template>
    <div>
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div>
                <h2 class="text-2xl font-bold text-slate-800">Reconciliation Reports</h2>
                <p class="text-sm text-slate-500 mt-1">Run and review roaming reconciliation results</p>
            </div>
            <div class="flex items-center gap-2">
                <button type="button" @click="handleExportSummary" :disabled="exportingSummary"
                    class="inline-flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-200 hover:border-green-300 hover:bg-green-50 text-slate-700 text-sm font-medium rounded-lg transition disabled:opacity-50">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5 5-5M12 15V3" />
                    </svg>
                    {{ exportingSummary ? 'Exporting...' : 'Export Summary' }}
                </button>
                <button type="button" @click="openCreate"
                    class="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    New Run
                </button>
            </div>
        </div>

        <!-- Error / Success -->
        <UiAlert v-if="error" variant="error" dismissible @dismiss="error = ''">{{ error }}</UiAlert>
        <UiAlert v-if="successMessage" variant="success" dismissible @dismiss="successMessage = ''">
            {{ successMessage }}
        </UiAlert>

        <!-- Summary cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            <UiStatCard label="Total Runs" :value="summary?.total_runs ?? '—'" accent="blue" />
            <UiStatCard label="Completed" :value="summary?.completed_runs ?? '—'" accent="green" />
            <UiStatCard label="Matched" :value="summary?.total_matched ?? '—'" accent="green" />
            <UiStatCard label="Mismatches" :value="summary?.total_mismatched ?? '—'" accent="amber" />
            <UiStatCard label="Unmatched" :value="summary?.total_unmatched ?? '—'" accent="red" />
        </div>

        <!-- Runs table -->
        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead class="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Run</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Status</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Records</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Matched</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Mismatched</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Unmatched</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Variance</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Created</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-if="loading">
                            <td colspan="9" class="px-2 py-2">
                                <UiSkeletonTable :rows="4" :cols="9" />
                            </td>
                        </tr>
                        <tr v-else-if="summary && summary.runs.length === 0">
                            <td colspan="9">
                                <UiEmptyState title="No reconciliation runs yet"
                                    description="Upload two CSV exports to compare your internal records against the partner statement." />
                            </td>
                        </tr>
                        <tr v-for="run in summary?.runs ?? []" :key="run.id" class="hover:bg-slate-50 transition">
                            <td class="px-4 py-3 font-medium text-slate-800 cursor-pointer" @click="openRun(run.id)">
                                {{ run.name }}
                                <span v-if="run.error_message"
                                    class="block text-xs text-slate-400 font-normal truncate max-w-[240px]"
                                    :title="run.error_message">
                                    {{ run.error_message }}
                                </span>
                            </td>
                            <td class="px-4 py-3">
                                <UiBadge :variant="statusVariant(run.status)">{{ run.status }}</UiBadge>
                            </td>
                            <td class="px-4 py-3 text-right text-slate-600">{{ run.total_records }}</td>
                            <td class="px-4 py-3 text-right text-emerald-600">{{ run.matched_records }}</td>
                            <td class="px-4 py-3 text-right text-amber-600">{{ run.mismatched_records }}</td>
                            <td class="px-4 py-3 text-right text-red-600">{{ run.unmatched_records }}</td>
                            <td class="px-4 py-3 text-right font-medium text-slate-800">
                                {{ formatAmount(run.total_variance) }}
                            </td>
                            <td class="px-4 py-3 text-slate-500 text-xs">{{ formatDateTime(run.created_at) }}</td>
                            <td class="px-4 py-3 text-right">
                                <div class="inline-flex items-center gap-1">
                                    <button type="button" @click="openRun(run.id)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition"
                                        title="View details">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                    <button type="button" @click="handleExportRun(run.id)"
                                        :disabled="exportingRunId === run.id"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-green-600 hover:bg-green-50 transition disabled:opacity-50"
                                        title="Download Excel">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5 5-5M12 15V3" />
                                        </svg>
                                    </button>
                                    <button type="button" @click="confirmDelete(run)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-red-600 hover:bg-red-50 transition"
                                        title="Delete">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- New Run Modal -->
        <UiModal :open="showModal" title="New Reconciliation Run"
            subtitle="Upload two CSV exports (reference, partner, date, duration_seconds, volume_kb, charge). Side A = internal records, Side B = partner statement."
            max-width="lg" @close="closeModal">
            <form @submit.prevent="handleSubmit" class="space-y-4">
                <!-- Name -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Run name</label>
                        <input v-model="form.name" type="text" required
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="e.g. September 2026 reconciliation" />
                    </div>

                    <!-- File inputs -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Side A (internal)</label>
                            <input ref="fileAInput" type="file" accept=".csv" required @change="onFileAChange"
                                class="w-full text-sm text-slate-600 file:mr-3 file:px-3 file:py-1.5 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 file:text-sm file:font-medium hover:file:bg-blue-100" />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Side B (partner)</label>
                            <input ref="fileBInput" type="file" accept=".csv" required @change="onFileBChange"
                                class="w-full text-sm text-slate-600 file:mr-3 file:px-3 file:py-1.5 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 file:text-sm file:font-medium hover:file:bg-blue-100" />
                        </div>
                    </div>

                    <!-- Form error -->
                    <div v-if="formError" class="p-2.5 rounded-lg bg-red-50 text-red-600 text-sm">
                        {{ formError }}
                    </div>

                    <!-- Actions -->
                    <div class="flex justify-end gap-2 pt-2">
                        <button type="button" @click="closeModal"
                            class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition">
                            Cancel
                        </button>
                        <button type="submit" :disabled="saving"
                            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg transition">
                            {{ saving ? 'Reconciling...' : 'Create & Reconcile' }}
                        </button>
                    </div>
            </form>
        </UiModal>

        <!-- Delete confirm -->
        <UiModal :open="deletingRun !== null" :title="`Delete Run`"
            :subtitle="`Are you sure you want to delete '${deletingRun?.name}'? All its records, matches and investigation cases will be removed.`"
            max-width="sm" @close="deletingRun = null">
            <div class="flex justify-end gap-2">
                <button type="button" @click="deletingRun = null"
                    class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition">
                    Cancel
                </button>
                <button type="button" @click="handleDelete" :disabled="saving"
                    class="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg transition">
                    {{ saving ? 'Deleting...' : 'Delete' }}
                </button>
            </div>
        </UiModal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
    getRunSummary,
    createRun,
    deleteRun,
    exportRunExcel,
    exportSummaryExcel,
    downloadBlob,
    formatAmount,
    formatDateTime,
    getErrorMessage,
} from '@/services/reconciliation'
import type { ReconciliationRun, RunSummary } from '@/types/reconciliation'
import { UiStatCard, UiBadge, UiModal, UiSkeletonTable, UiEmptyState, UiAlert } from '@/components/ui'

const router = useRouter()

const summary = ref<RunSummary | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const successMessage = ref('')
const showModal = ref(false)
const deletingRun = ref<ReconciliationRun | null>(null)
const exportingRunId = ref<number | null>(null)
const exportingSummary = ref(false)

const form = ref({
    name: '',
    fileA: null as File | null,
    fileB: null as File | null,
})
const fileAInput = ref<HTMLInputElement | null>(null)
const fileBInput = ref<HTMLInputElement | null>(null)
const formError = ref('')

const statusVariant = (status: string) =>
    status === 'completed'
        ? 'success'
        : status === 'failed'
          ? 'danger'
          : status === 'running'
            ? 'warning'
            : 'neutral'

const loadSummary = async (): Promise<void> => {
    loading.value = true
    error.value = ''
    try {
        summary.value = await getRunSummary()
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        loading.value = false
    }
}

const openRun = (runId: number): void => {
    router.push(`/reports/runs/${runId}`)
}

const openCreate = (): void => {
    form.value.name = ''
    form.value.fileA = null
    form.value.fileB = null
    formError.value = ''
    showModal.value = true
}

const closeModal = (): void => {
    showModal.value = false
    form.value.name = ''
    form.value.fileA = null
    form.value.fileB = null
    formError.value = ''
    if (fileAInput.value) fileAInput.value.value = ''
    if (fileBInput.value) fileBInput.value.value = ''
}

const onFileAChange = (event: Event): void => {
    form.value.fileA = (event.target as HTMLInputElement).files?.[0] ?? null
}

const onFileBChange = (event: Event): void => {
    form.value.fileB = (event.target as HTMLInputElement).files?.[0] ?? null
}

const handleSubmit = async (): Promise<void> => {
    if (!form.value.fileA || !form.value.fileB) {
        formError.value = 'Please select both CSV files.'
        return
    }

    saving.value = true
    formError.value = ''

    try {
        const run = await createRun(form.value.name, form.value.fileA, form.value.fileB)
        closeModal()
        successMessage.value = `Run "${run.name}" completed: ${run.matched_records} matched, ${run.mismatched_records} mismatched, ${run.unmatched_records} unmatched.`
        await loadSummary()
    } catch (err) {
        formError.value = await getErrorMessage(err)
    } finally {
        saving.value = false
    }
}

const handleExportRun = async (runId: number): Promise<void> => {
    exportingRunId.value = runId
    error.value = ''
    try {
        const blob = await exportRunExcel(runId)
        downloadBlob(blob, `reconciliation_run_${runId}.xlsx`)
        successMessage.value = `Excel report for run #${runId} downloaded.`
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        exportingRunId.value = null
    }
}

const handleExportSummary = async (): Promise<void> => {
    exportingSummary.value = true
    error.value = ''
    try {
        const blob = await exportSummaryExcel()
        downloadBlob(blob, 'reconciliation_summary.xlsx')
        successMessage.value = 'Summary Excel downloaded.'
    } catch (err) {
        error.value = await getErrorMessage(err)
    } finally {
        exportingSummary.value = false
    }
}

const confirmDelete = (run: ReconciliationRun): void => {
    deletingRun.value = run
}

const handleDelete = async (): Promise<void> => {
    if (!deletingRun.value) return
    saving.value = true
    try {
        await deleteRun(deletingRun.value.id)
        successMessage.value = `Run "${deletingRun.value.name}" deleted.`
        deletingRun.value = null
        await loadSummary()
    } catch (err) {
        error.value = await getErrorMessage(err)
        deletingRun.value = null
    } finally {
        saving.value = false
    }
}

onMounted(loadSummary)
</script>
