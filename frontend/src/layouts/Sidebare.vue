<template>
    <aside
        class="flex flex-col h-screen bg-slate-900 text-slate-300 transition-all duration-300 ease-in-out flex-shrink-0"
        :class="collapsed ? 'w-[72px]' : 'w-64'">

        <!-- Brand -->
        <div class="flex items-center h-16 px-4 border-b border-slate-800">
            <div v-if="!collapsed" class="flex items-center gap-2.5 min-w-0">
                <div
                    class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shrink-0">
                    <!-- <svg class="w-[18px] h-[18px] text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg> -->

                    <img src="../../public/logo.jpg" alt="">
                </div>
                <div class="min-w-0">
                    <p class="text-sm font-bold text-white leading-tight truncate">Roaming Portal</p>
                    <p class="text-[10px] text-slate-400 leading-tight">Reconciliation Suite</p>
                </div>
            </div>
            <div v-else
                class="w-8 h-8 mx-auto rounded-lg bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
                <svg class="w-[18px] h-[18px] text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-3 py-4 space-y-6 overflow-y-auto">
            <div v-for="group in menuGroups" :key="group.label">
                <!-- Section label -->
                <p v-if="!collapsed"
                    class="px-3 mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                    {{ group.label }}
                </p>
                <div v-else class="mx-3 mb-2 border-t border-slate-800" />

                <div class="space-y-1">
                    <RouterLink v-for="item in group.items" :key="item.to" :to="item.to"
                        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
                        :class="{ '!bg-blue-600 !text-white': isActive(item.to) }"
                        :title="collapsed ? item.label : undefined">
                        <span class="w-5 h-5 flex-shrink-0" v-html="item.icon"></span>
                        <span v-if="!collapsed" class="text-sm font-medium truncate">
                            {{ item.label }}
                        </span>
                    </RouterLink>
                </div>
            </div>
        </nav>

        <!-- Footer: user -->
        <div class="border-t border-slate-800 px-3 py-3">
            <div class="flex items-center gap-3 rounded-lg px-2 py-1.5" :class="collapsed ? 'justify-center' : ''">
                <div
                    class="w-9 h-9 rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center shrink-0 ring-1 ring-slate-600">
                    <span class="text-xs font-bold text-white">{{ userInitials }}</span>
                </div>
                <div v-if="!collapsed" class="min-w-0 flex-1">
                    <p class="text-xs font-semibold text-slate-200 truncate">{{ userName }}</p>
                    <p class="text-[10px] text-slate-500 truncate">{{ userRole }}</p>
                </div>
            </div>
            <p v-if="!collapsed" class="mt-2 px-2 text-[10px] text-slate-600 leading-tight">
                Develop By DIN Leader
            </p>
        </div>
    </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import type { MenuItem } from '@/types/layout'

defineProps<{
    collapsed?: boolean
}>()

const route = useRoute()

const user = computed(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
})

const userName = computed(() => user.value?.name ?? 'User')

const userRole = computed(() => {
    const roles: string[] = user.value?.roles ?? []
    return roles.length > 0 ? roles[0] : 'Member'
})

const userInitials = computed(() =>
    userName.value
        .split(' ')
        .map((part: string) => part[0])
        .slice(0, 2)
        .join('')
        .toUpperCase(),
)

interface MenuGroup {
    label: string
    items: MenuItem[]
}

const menuGroups: MenuGroup[] = [
    {
        label: 'Overview',
        items: [
            {
                to: '/',
                label: 'Dashboard',
                icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"/></svg>`,
            },
        ],
    },
    {
        label: 'Workspace',
        items: [
            {
                to: '/reports',
                label: 'Reports',
                icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>`,
            },
            {
                to: '/operations',
                label: 'Operations',
                icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h10"/>
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 16v4m-2-2h4"/>
  </svg>`,
            },
        ],
    },
    {
        label: 'Administration',
        items: [
            {
                to: '/settings',
                label: 'Settings',
                icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`,
            },
        ],
    },
]

/** Exact match for `/`, prefix match for nested routes like /settings/* */
const isActive = (path: string): boolean => {
    if (path === '/') {
        return route.path === '/'
    }
    return route.path === path || route.path.startsWith(path + '/')
}
</script>
