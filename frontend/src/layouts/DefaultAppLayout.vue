<template>
    <div class="flex min-h-screen bg-slate-50">
        <!-- Sidebar -->
        <Sidebare :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

        <!-- Mobile overlay -->
        <div v-if="!sidebarCollapsed && isMobile" class="fixed inset-0 z-30 bg-black/40 md:hidden"
            @click="sidebarCollapsed = true" />

        <!-- Main area -->
        <div class="flex flex-col flex-1 min-w-0">
            <Navbar :title="pageTitle" @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />

            <main class="flex-1 p-4 md:p-6 overflow-y-auto">
                <RouterView />
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
// import Sidebare from './Sidebare.vue'
import Sidebare from './Sidebare.vue'
import Navbar from './Navbar.vue'

const sidebarCollapsed = ref(false)
const isMobile = ref(false)
const route = useRoute()

const pageTitle = computed(() => {
    const titles: Record<string, string> = {
        '/': 'Dashboard',
        '/reports': 'Reports',
        '/settings/users': 'Settings',
        '/settings/roles': 'Settings',
        '/settings/permissions': 'Settings',
    }
    return titles[route.path] ?? 'Page'
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