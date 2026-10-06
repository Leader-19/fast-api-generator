<script setup lang="ts">
import { watch, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
    open: boolean
    title: string
    subtitle?: string
    maxWidth?: 'sm' | 'md' | 'lg'
}>()

const emit = defineEmits<{
    close: []
}>()

const handleKeydown = (e: KeyboardEvent): void => {
    if (e.key === 'Escape' && props.open) {
        emit('close')
    }
}

const lockScroll = (lock: boolean): void => {
    document.body.style.overflow = lock ? 'hidden' : ''
}

onMounted(() => {
    document.addEventListener('keydown', handleKeydown)
    if (props.open) lockScroll(true)
})

onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
    lockScroll(false)
})

watch(
    () => props.open,
    (open) => lockScroll(open),
)
</script>

<template>
    <Teleport to="body">
        <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/40" @click="emit('close')" />
            <div
                class="relative w-full bg-white rounded-2xl shadow-xl p-6"
                :class="maxWidth === 'lg' ? 'max-w-lg' : maxWidth === 'sm' ? 'max-w-sm' : 'max-w-md'"
                role="dialog"
                aria-modal="true"
            >
                <div class="flex items-start justify-between gap-4 mb-4">
                    <div>
                        <h3 class="text-lg font-semibold text-slate-800">{{ title }}</h3>
                        <p v-if="subtitle" class="text-sm text-slate-500 mt-0.5">{{ subtitle }}</p>
                    </div>
                    <button
                        type="button"
                        class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
                        aria-label="Close"
                        @click="emit('close')"
                    >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <slot />
            </div>
        </div>
    </Teleport>
</template>
