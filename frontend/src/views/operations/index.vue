<template>
    <div>
        <!-- Header -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-slate-800">Operations</h2>
            <p class="text-sm text-slate-500 mt-1">
                Manage All Operations Functions
            </p>
        </div>

        <!-- Cards grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <button v-for="card in cards" :key="card.to" type="button" @click="goTo(card.to)" class="group text-left bg-white border border-slate-200 rounded-2xl p-6
               hover:border-blue-300 hover:shadow-md transition-all duration-200
               focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                <!-- Icon -->
                <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-colors"
                    :class="card.iconBg">
                    <span class="w-6 h-6" :class="card.iconColor" v-html="card.icon"></span>
                </div>

                <!-- Text -->
                <h3 class="text-base font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                    {{ card.title }}
                </h3>
                <p class="text-sm text-slate-500 mt-1 leading-relaxed">
                    {{ card.description }}
                </p>

                <!-- Arrow -->
                <div
                    class="mt-4 flex items-center gap-1 text-sm font-medium text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity">
                    Open
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                </div>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const cards = [
    {
        to: '/settings/users',
        title: 'RA Reports',
        description: 'Create, edit and manage system users and their access.',
        iconBg: 'bg-blue-50 group-hover:bg-blue-100',
        iconColor: 'text-blue-600',
        icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>`,
    },
    {
        to: '/operations/pdf',
        title: 'PDF Generator',
        description: 'Define roles and assign permissions to control access.',
        iconBg: 'bg-violet-50 group-hover:bg-violet-100',
        iconColor: 'text-violet-600',
        icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`,
    },
    {
        to: '/settings/permissions',
        title: 'Excel Generator',
        description: 'View all system permissions discovered from the API.',
        iconBg: 'bg-emerald-50 group-hover:bg-emerald-100',
        iconColor: 'text-emerald-600',
        icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>`,
    },
    {
        to: '/settings/permissions',
        title: 'Word Generator',
        description: 'View all system permissions discovered from the API.',
        iconBg: 'bg-emerald-50 group-hover:bg-emerald-100',
        iconColor: 'text-emerald-600',
        icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>`,
    },
]

const goTo = (path: string): void => {
    router.push(path)
}
</script>