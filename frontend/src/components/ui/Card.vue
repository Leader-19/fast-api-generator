<script setup lang="ts">
defineProps<{
    as?: 'div' | 'section' | 'article'
    padded?: boolean
}>()
</script>

<template>
    <component
        :is="as ?? 'div'"
        class="bg-white border border-slate-200 rounded-2xl shadow-sm"
        :class="padded === false ? '' : 'p-5 md:p-6'"
    >
        <slot />
    </component>
</template>
