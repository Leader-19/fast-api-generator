<script setup lang="ts">
withDefaults(
    defineProps<{
        variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral'
        size?: 'sm' | 'md'
    }>(),
    {
        variant: 'neutral',
        size: 'md',
    },
)
</script>

<template>
    <span
        class="inline-flex items-center rounded-full font-medium"
        :class="[
            variant === 'success' ? 'bg-emerald-50 text-emerald-700' : '',
            variant === 'warning' ? 'bg-amber-50 text-amber-700' : '',
            variant === 'danger' ? 'bg-red-50 text-red-700' : '',
            variant === 'info' ? 'bg-blue-50 text-blue-700' : '',
            variant === 'neutral' ? 'bg-slate-100 text-slate-500' : '',
            size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs',
        ]"
    >
        <slot />
    </span>
</template>
