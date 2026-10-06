<script setup lang="ts">
withDefaults(
    defineProps<{
        rows?: number
        cols?: number
    }>(),
    {
        rows: 5,
        cols: 6,
    },
)
</script>

<template>
    <div class="animate-pulse divide-y divide-slate-100">
        <div v-for="row in rows" :key="row" class="flex items-center gap-4 px-4 py-3.5">
            <div
                v-for="col in cols"
                :key="col"
                class="h-3.5 rounded bg-slate-200"
                :class="col === 1 ? 'w-32' : col === 2 ? 'w-20' : 'flex-1 max-w-[120px]'"
            />
        </div>
    </div>
</template>
