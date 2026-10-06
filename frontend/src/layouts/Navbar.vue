<template>
    <header
        class="sticky top-0 z-20 flex items-center justify-between h-16 px-4 md:px-6 bg-white border-b border-slate-200">
        <!-- Left -->
        <div class="flex items-center gap-3">
            <button type="button" @click="emit('toggle-sidebar')"
                class="p-2 rounded-lg text-slate-600 hover:bg-slate-100 md:hidden" aria-label="Open menu">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>

            <h1 class="text-lg font-semibold text-slate-800">
                {{ title }}
            </h1>
        </div>

        <!-- Right -->
        <div class="flex items-center gap-3 md:gap-5">
            <!-- Search -->
            <div class="hidden sm:block relative">
                <input type="search" placeholder="Search..." class="w-48 lg:w-64 pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg
                 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none"
                    stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </div>


            <!-- User dropdown -->
            <div class="relative" ref="dropdownRef">
                <button type="button" @click="isOpen = !isOpen" class="flex items-center gap-2.5 cursor-pointer group">
                    <img src="../../public/logo.jpg" alt="User avatar"
                        class="w-9 h-9 rounded-full object-cover ring-2 ring-transparent group-hover:ring-blue-500 transition" />
                    <span class="hidden md:block text-sm font-medium text-slate-700">
                        {{ userName }}
                    </span>
                    <svg class="w-4 h-4 text-slate-400 hidden md:block transition-transform"
                        :class="{ 'rotate-180': isOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                <!-- Dropdown menu -->
                <div v-if="isOpen"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-slate-100 py-1 z-50">
                    <div class="px-4 py-2 border-b border-slate-100">
                        <p class="text-sm font-medium text-slate-800 truncate">{{ userName }}</p>
                        <p class="text-xs text-slate-500 truncate">{{ userEmail }}</p>
                    </div>

                    <button type="button" @click="handleLogout"
                        class="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Logout
                    </button>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { logout } from '@/services/auth'

withDefaults(
    defineProps<{
        title?: string
    }>(),
    {
        title: 'Dashboard',
    }
)

const emit = defineEmits<{
    'toggle-sidebar': []
}>()

const router = useRouter()
const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

// Get user info from localStorage
const user = computed(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
})

const userName = computed(() => user.value?.name ?? 'User')
const userEmail = computed(() => user.value?.email ?? '')
const userAvatar = computed(() => user.value?.avatar ?? 'https://i.pravatar.cc/40')

const handleLogout = (): void => {
    isOpen.value = false
    logout()
    router.push({ name: 'Login' })
}

// Close dropdown when clicking outside
const handleClickOutside = (e: MouseEvent): void => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
        isOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>