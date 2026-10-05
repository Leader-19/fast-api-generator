<template>
  <aside
    class="flex flex-col h-screen bg-slate-900 text-slate-300 transition-all duration-300 ease-in-out flex-shrink-0"
    :class="collapsed ? 'w-[72px]' : 'w-64'">
    <!-- Brand -->
    <div class="flex items-center justify-between h-16 px-4 border-b border-slate-800">
      <span v-if="!collapsed" class="text-lg font-bold text-white tracking-wide">
        Roaming Web Portal
      </span>
      <button type="button" @click="emit('toggle')"
        class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        aria-label="Toggle sidebar">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
      <RouterLink v-for="item in menu" :key="item.to" :to="item.to"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
        :class="{ '!bg-blue-600 !text-white': isActive(item.to) }">
        <span class="w-5 h-5 flex-shrink-0" v-html="item.icon"></span>
        <span v-if="!collapsed" class="text-sm font-medium truncate">
          {{ item.label }}
        </span>
      </RouterLink>
    </nav>

    <!-- Footer -->
    <div v-if="!collapsed" class="px-4 py-3 border-t border-slate-800 text-xs text-slate-500">
      Develop By DIN Leader
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import type { MenuItem } from '@/types/layout'

defineProps<{
  collapsed?: boolean
}>()

const emit = defineEmits<{
  toggle: []
}>()

const route = useRoute()

const menu: MenuItem[] = [
  {
    to: '/',
    label: 'Dashboard',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"/></svg>`,
  },
  {
    to: '/operations',
    label: 'Operations',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h10"/>
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 16v4m-2-2h4"/>
  </svg>`,
  },
  {
    to: '/settings',
    label: 'Settings',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`,
  },

  {
    to: '/reports',
    label: 'Reports',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>`,
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