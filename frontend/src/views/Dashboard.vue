<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
    getRunSummary,
    formatAmount,
    formatDateTime,
    getErrorMessage,
} from '@/services/reconciliation'
import type { ReconciliationRun, RunSummary } from '@/types/reconciliation'
import { UiStatCard, UiBadge, UiCard, UiEmptyState, UiAlert } from '@/components/ui'

const router = useRouter()

const summary = ref<RunSummary | null>(null)
const loading = ref(false)
const error = ref('')

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

const latestRuns = computed<ReconciliationRun[]>(() =>
    (summary.value?.runs ?? []).slice(0, 5),
)

const totalRecords = computed(() =>
    (summary.value?.runs ?? [])
        .filter((r) => r.status === 'completed')
        .reduce((acc, r) => acc + r.total_records, 0),
)

const matchRate = computed<number | null>(() => {
    const matched = summary.value?.total_matched ?? 0
    const mismatched = summary.value?.total_mismatched ?? 0
    const unmatched = summary.value?.total_unmatched ?? 0
    const total = matched + mismatched + unmatched
    return total === 0 ? null : Math.round((matched / total) * 100)
})

const proportionSegments = computed(() => {
    const s = summary.value
    const matched = s?.total_matched ?? 0
    const mismatched = s?.total_mismatched ?? 0
    const unmatched = s?.total_unmatched ?? 0
    const total = matched + mismatched + unmatched

    if (total === 0) {
        return []
    }

    const pct = (n: number) => (n / total) * 100

    return [
        { key: 'matched', label: 'Matched', count: matched, percent: pct(matched), bar: 'bg-emerald-500', dot: 'bg-emerald-500' },
        { key: 'mismatched', label: 'Mismatched', count: mismatched, percent: pct(mismatched), bar: 'bg-amber-400', dot: 'bg-amber-400' },
        { key: 'unmatched', label: 'Unmatched', count: unmatched, percent: pct(unmatched), bar: 'bg-red-400', dot: 'bg-red-400' },
    ].filter((segment) => segment.count > 0)
})

const ICONS = {
    runs: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>',
    matched: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    mismatch: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
    variance: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    records: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/></svg>',
    newRun: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>',
    reports: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>',
    empty: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>',
}

const runStatusVariant = (status: string) =>
    status === 'completed'
        ? 'success'
        : status === 'failed'
          ? 'danger'
          : status === 'running'
            ? 'warning'
            : 'neutral'

const openRun = (id: number): void => {
    router.push(`/reports/runs/${id}`)
}

onMounted(loadSummary)
</script>

<template>
    <div class="space-y-6">
        <!-- Welcome -->
        <div>
            <h2 class="text-2xl font-bold text-slate-800">Welcome back</h2>
            <p class="text-sm text-slate-500 mt-1">
                Here's an overview of your roaming reconciliation activity.
            </p>
        </div>

        <UiAlert v-if="error" variant="error" dismissible @dismiss="error = ''">
            {{ error }}
        </UiAlert>

        <!-- KPI cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <UiStatCard label="Total Runs" :value="summary?.total_runs ?? '—'" :icon="ICONS.runs" accent="blue"
                hint="all time" />
            <UiStatCard label="Matched" :value="summary?.total_matched ?? '—'" :icon="ICONS.matched" accent="green"
                :hint="matchRate !== null ? `${matchRate}% match rate` : 'no data yet'" />
            <UiStatCard label="Mismatches" :value="summary?.total_mismatched ?? '—'" :icon="ICONS.mismatch"
                accent="amber" hint="needs review" />
            <UiStatCard label="Unmatched" :value="summary?.total_unmatched ?? '—'" :icon="ICONS.mismatch" accent="red"
                hint="one-sided records" />
            <UiStatCard label="Total Variance" :value="formatAmount(summary?.total_variance ?? 0)" :icon="ICONS.variance"
                accent="slate" :hint="`${totalRecords} records processed`" />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Result proportion -->
            <UiCard class="lg:col-span-1">
                <h3 class="text-sm font-semibold text-slate-800">Reconciliation Results</h3>
                <p class="text-xs text-slate-400 mt-0.5">across all completed runs</p>

                <template v-if="proportionSegments.length > 0">
                    <div class="mt-5 flex h-3 w-full overflow-hidden rounded-full bg-slate-100">
                        <div v-for="segment in proportionSegments" :key="segment.key" class="h-full"
                            :class="segment.bar" :style="{ width: `${segment.percent}%` }" />
                    </div>

                    <ul class="mt-4 space-y-2.5">
                        <li v-for="segment in proportionSegments" :key="segment.key"
                            class="flex items-center gap-2 text-sm">
                            <span class="w-2.5 h-2.5 rounded-full shrink-0" :class="segment.dot" />
                            <span class="text-slate-600 flex-1">{{ segment.label }}</span>
                            <span class="font-medium text-slate-800 tabular-nums">{{ segment.count }}</span>
                            <span class="text-xs text-slate-400 w-12 text-right tabular-nums">
                                {{ segment.percent.toFixed(0) }}%
                            </span>
                        </li>
                    </ul>
                </template>

                <p v-else class="mt-6 text-sm text-slate-400 text-center py-8">
                    Run a reconciliation to see results here.
                </p>

                <button type="button" @click="router.push('/reports')"
                    class="mt-6 w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition">
                    <span class="w-4 h-4" v-html="ICONS.newRun" />
                    New Reconciliation
                </button>
            </UiCard>

            <!-- Latest runs -->
            <UiCard class="lg:col-span-2" :padded="false">
                <div class="flex items-center justify-between px-5 md:px-6 pt-5 md:pt-6 pb-4">
                    <div>
                        <h3 class="text-sm font-semibold text-slate-800">Latest Runs</h3>
                        <p class="text-xs text-slate-400 mt-0.5">most recent reconciliations</p>
                    </div>
                    <button type="button" @click="router.push('/reports')"
                        class="text-sm font-medium text-blue-600 hover:text-blue-700 transition">
                        View all
                    </button>
                </div>

                <div v-if="loading" class="animate-pulse divide-y divide-slate-100">
                    <div v-for="i in 4" :key="i" class="flex items-center gap-4 px-5 md:px-6 py-3.5">
                        <div class="h-3.5 w-40 rounded bg-slate-200" />
                        <div class="h-3.5 w-16 rounded bg-slate-200 ml-auto" />
                        <div class="h-3.5 w-20 rounded bg-slate-200" />
                    </div>
                </div>

                <div v-else-if="latestRuns.length === 0">
                    <UiEmptyState title="No runs yet" description="Create your first reconciliation run to see it here."
                        :icon="ICONS.empty">
                        <button type="button" @click="router.push('/reports')"
                            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
                            Go to Reports
                        </button>
                    </UiEmptyState>
                </div>

                <ul v-else class="divide-y divide-slate-100">
                    <li v-for="run in latestRuns" :key="run.id">
                        <button type="button" @click="openRun(run.id)"
                            class="w-full flex items-center gap-4 px-5 md:px-6 py-3.5 hover:bg-slate-50 transition text-left">
                            <div class="min-w-0 flex-1">
                                <p class="text-sm font-medium text-slate-800 truncate">{{ run.name }}</p>
                                <p class="text-xs text-slate-400 mt-0.5">{{ formatDateTime(run.created_at) }}</p>
                            </div>
                            <div class="hidden sm:flex items-center gap-5 text-xs tabular-nums">
                                <span class="text-emerald-600 font-medium">{{ run.matched_records }} matched</span>
                                <span class="text-amber-600 font-medium">{{ run.mismatched_records }} mismatched</span>
                                <span class="text-red-600 font-medium">{{ run.unmatched_records }} unmatched</span>
                            </div>
                            <UiBadge :variant="runStatusVariant(run.status)">{{ run.status }}</UiBadge>
                            <svg class="w-4 h-4 text-slate-300 shrink-0" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                    </li>
                </ul>
            </UiCard>
        </div>

        <!-- Quick actions -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button type="button" @click="router.push('/reports')"
                class="group text-left bg-white border border-slate-200 rounded-2xl p-5 hover:border-blue-300 hover:shadow-md transition-all">
                <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
                    <span class="w-5 h-5" v-html="ICONS.newRun" />
                </div>
                <h4 class="text-sm font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                    New Reconciliation
                </h4>
                <p class="text-xs text-slate-500 mt-1">Upload two CSV files and compare records.</p>
            </button>

            <button type="button" @click="router.push('/reports')"
                class="group text-left bg-white border border-slate-200 rounded-2xl p-5 hover:border-emerald-300 hover:shadow-md transition-all">
                <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3">
                    <span class="w-5 h-5" v-html="ICONS.reports" />
                </div>
                <h4 class="text-sm font-semibold text-slate-800 group-hover:text-emerald-600 transition-colors">
                    Browse Reports
                </h4>
                <p class="text-xs text-slate-500 mt-1">Review results, filter matches and export Excel.</p>
            </button>

            <button type="button" @click="router.push('/operations/pdf')"
                class="group text-left bg-white border border-slate-200 rounded-2xl p-5 hover:border-violet-300 hover:shadow-md transition-all">
                <div class="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center mb-3">
                    <span class="w-5 h-5" v-html="ICONS.records" />
                </div>
                <h4 class="text-sm font-semibold text-slate-800 group-hover:text-violet-600 transition-colors">
                    PDF Converter
                </h4>
                <p class="text-xs text-slate-500 mt-1">Convert PDF reports into Excel or Word files.</p>
            </button>
        </div>
    </div>
</template>
