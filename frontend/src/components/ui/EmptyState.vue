<script setup lang="ts">
defineProps<{
    icon?: string
    title: string
    description?: string
}>()
</script>

<template>
    <div class="flex flex-col items-center justify-center text-center py-14 px-6">
        <div class="w-14 h-14 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
            <span v-if="icon" class="w-7 h-7 text-slate-400" v-html="icon" />
        </div>
        <h3 class="text-base font-semibold text-slate-700">{{ title }}</h3>
        <p v-if="description" class="text-sm text-slate-400 mt-1 max-w-sm leading-relaxed">
            {{ description }}
        </p>
        <div v-if="$slots.default" class="mt-5">
            <slot />
        </div>
    </div>
</template>
