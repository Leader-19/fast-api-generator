<script setup lang="ts">
withDefaults(
    defineProps<{
        variant?: 'error' | 'success' | 'info'
        dismissible?: boolean
    }>(),
    {
        variant: 'info',
        dismissible: false,
    },
)

const emit = defineEmits<{
    dismiss: []
}>()

const ICONS: Record<string, string> = {
    error:
        'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    success: 'M5 13l4 4L19 7',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
}

const CLASSES: Record<string, string> = {
    error: 'bg-red-50 border-red-100 text-red-600',
    success: 'bg-green-50 border-green-100 text-green-700',
    info: 'bg-blue-50 border-blue-100 text-blue-700',
}
</script>

<template>
    <div class="mb-4 flex items-start gap-3 p-3 rounded-lg border text-sm" :class="CLASSES[variant]">
        <svg class="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="ICONS[variant]" />
        </svg>
        <div class="flex-1 min-w-0">
            <slot />
        </div>
        <button
            v-if="dismissible"
            type="button"
            class="shrink-0 opacity-60 hover:opacity-100 transition"
            aria-label="Dismiss"
            @click="emit('dismiss')"
        >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
</template>
