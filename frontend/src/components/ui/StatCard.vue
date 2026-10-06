<script setup lang="ts">
withDefaults(
    defineProps<{
        label: string
        value: string | number
        hint?: string
        accent?: 'blue' | 'green' | 'amber' | 'red' | 'slate'
        icon?: string
    }>(),
    {
        hint: undefined,
        accent: 'slate',
        icon: undefined,
    },
)

const ICON_BG: Record<string, string> = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-emerald-50 text-emerald-600',
    amber: 'bg-amber-50 text-amber-600',
    red: 'bg-red-50 text-red-600',
    slate: 'bg-slate-100 text-slate-600',
}
</script>

<template>
    <div class="bg-white border border-slate-200 rounded-2xl p-4 md:p-5 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wide truncate">{{ label }}</p>
                <p class="text-2xl font-bold text-slate-800 mt-1.5 tabular-nums">{{ value }}</p>
                <p v-if="hint" class="text-xs text-slate-400 mt-1 truncate">{{ hint }}</p>
            </div>
            <div
                v-if="icon"
                class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                :class="ICON_BG[accent]"
            >
                <span class="w-5 h-5" v-html="icon" />
            </div>
        </div>
        <slot />
    </div>
</template>
