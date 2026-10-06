<template>
    <div class="flex h-screen overflow-hidden bg-slate-50">
        <!-- Sidebar -->
        <Sidebare :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

        <!-- Mobile overlay -->
        <div v-if="!sidebarCollapsed && isMobile" class="fixed inset-0 z-30 bg-black/40 md:hidden"
            @click="sidebarCollapsed = true" />

        <!-- Main area -->
        <div class="flex flex-1 min-w-0 flex-col h-screen overflow-hidden">
            <!-- Navbar -->
            <Navbar :title="pageTitle" @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />

            <!-- Only this area scrolls -->
            <main class="flex-1 min-h-0 overflow-y-auto p-4 md:p-6">
                <RouterView />
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebare from './Sidebare.vue'
import Navbar from './Navbar.vue'

const sidebarCollapsed = ref(false)
const isMobile = ref(false)
const route = useRoute()

const pageTitle = computed(() => {
    const to = route.matched[route.matched.length - 1]

    const title = to?.meta?.title as string | undefined

    if (title) {
        return title
    }

    return route.path === '/'
        ? 'Dashboard'
        : 'Settings'
})

const checkMobile = (): void => {
    isMobile.value = window.innerWidth < 768

    if (isMobile.value) {
        sidebarCollapsed.value = true
    }
}

onMounted(() => {
    checkMobile()
    window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
    window.removeEventListener('resize', checkMobile)
})
</script>