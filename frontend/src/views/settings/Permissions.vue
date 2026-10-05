<template>
    <div>
        <div class="mb-4">
            <button type="button" @click="$router.push('/settings')"
                class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Back to Settings
            </button>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div>
                <h3 class="text-lg font-semibold text-slate-800">Permissions</h3>
                <p class="text-sm text-slate-500">
                    Permissions are synced from the backend seeder / scanner
                </p>
            </div>
            <button type="button" @click="load" :disabled="loading"
                class="inline-flex items-center gap-2 px-4 py-2.5 border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-medium rounded-lg transition">
                <svg class="w-4 h-4" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Refresh
            </button>
        </div>

        <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm border border-red-100">
            {{ error }}
        </div>

        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <table class="w-full text-sm">
                <thead class="bg-slate-50 border-b border-slate-200">
                    <tr>
                        <th class="text-left px-4 py-3 font-medium text-slate-600">ID</th>
                        <th class="text-left px-4 py-3 font-medium text-slate-600">Permission</th>
                        <th class="text-left px-4 py-3 font-medium text-slate-600">Group</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                    <tr v-if="loading">
                        <td colspan="3" class="px-4 py-8 text-center text-slate-400">Loading...</td>
                    </tr>
                    <tr v-else-if="permissions.length === 0">
                        <td colspan="3" class="px-4 py-8 text-center text-slate-400">
                            No permissions. Run: <code class="text-slate-600">python -m app.seeders.seed</code>
                        </td>
                    </tr>
                    <tr v-for="perm in permissions" :key="perm.id" class="hover:bg-slate-50">
                        <td class="px-4 py-3 text-slate-500">{{ perm.id }}</td>
                        <td class="px-4 py-3 font-mono text-slate-800">{{ perm.name }}</td>
                        <td class="px-4 py-3">
                            <span class="px-2 py-0.5 text-xs rounded-full bg-slate-100 text-slate-600">
                                {{ perm.name.split('.')[0] }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// import { getPermissions } from '@/services/roles'
// import type { Permission } from '@/types/role'

import type { Permission } from '@/types/role'
import { getPermissions } from '../../services/roles'
const permissions = ref<Permission[]>([])
const loading = ref(false)
const error = ref('')

const load = async (): Promise<void> => {
    loading.value = true
    error.value = ''
    try {
        permissions.value = await getPermissions()
    } catch (err: any) {
        error.value = err.response?.data?.detail ?? 'Failed to load permissions'
    } finally {
        loading.value = false
    }
}

onMounted(() => load())
</script>