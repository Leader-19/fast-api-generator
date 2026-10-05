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
                <h3 class="text-lg font-semibold text-slate-800">Roles</h3>
                <p class="text-sm text-slate-500">Create roles and assign permissions</p>
            </div>
            <button type="button" @click="openCreate"
                class="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Role
            </button>
        </div>

        <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm border border-red-100">
            {{ error }}
        </div>

        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead class="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">ID</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Name</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Description</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Permissions</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-if="loading">
                            <td colspan="5" class="px-4 py-8 text-center text-slate-400">Loading roles...</td>
                        </tr>
                        <tr v-else-if="roles.length === 0">
                            <td colspan="5" class="px-4 py-8 text-center text-slate-400">No roles found</td>
                        </tr>
                        <tr v-for="role in roles" :key="role.id" class="hover:bg-slate-50 transition">
                            <td class="px-4 py-3 text-slate-500">{{ role.id }}</td>
                            <td class="px-4 py-3 font-medium text-slate-800">{{ role.name }}</td>
                            <td class="px-4 py-3 text-slate-600">{{ role.description || '—' }}</td>
                            <td class="px-4 py-3">
                                <div class="flex flex-wrap gap-1 max-w-md">
                                    <span v-for="perm in role.permissions" :key="perm"
                                        class="px-2 py-0.5 text-xs rounded-full bg-violet-50 text-violet-700">
                                        {{ perm }}
                                    </span>
                                    <span v-if="!role.permissions?.length" class="text-slate-400 text-xs">—</span>
                                </div>
                            </td>
                            <td class="px-4 py-3 text-right">
                                <div class="inline-flex items-center gap-1">
                                    <button type="button" @click="openEdit(role)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition"
                                        title="Edit">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button type="button" @click="confirmDelete(role)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-red-600 hover:bg-red-50 transition disabled:opacity-40"
                                        title="Delete" :disabled="role.name === 'ADMIN'">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/40" @click="closeModal" />
            <div class="relative w-full max-w-lg bg-white rounded-2xl shadow-xl p-6 max-h-[90vh] overflow-y-auto">
                <h3 class="text-lg font-semibold text-slate-800 mb-4">
                    {{ editingRole ? 'Edit Role' : 'Create Role' }}
                </h3>

                <form @submit.prevent="handleSubmit" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Name</label>
                        <input v-model="form.name" type="text" required :disabled="editingRole?.name === 'ADMIN'"
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-50"
                            placeholder="e.g. ANALYST" />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Description</label>
                        <input v-model="form.description" type="text"
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Optional description" />
                    </div>

                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <label class="block text-sm font-medium text-slate-700">Permissions</label>
                            <div class="flex gap-2 text-xs">
                                <button type="button" @click="selectAll" class="text-blue-600 hover:underline">
                                    Select all
                                </button>
                                <button type="button" @click="form.permission_ids = []"
                                    class="text-slate-500 hover:underline">
                                    Clear
                                </button>
                            </div>
                        </div>
                        <div
                            class="border border-slate-200 rounded-lg max-h-56 overflow-y-auto divide-y divide-slate-100">
                            <label v-for="perm in permissions" :key="perm.id"
                                class="flex items-center gap-3 px-3 py-2.5 cursor-pointer hover:bg-slate-50">
                                <input type="checkbox" :value="perm.id" v-model="form.permission_ids"
                                    class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                                <span class="text-sm text-slate-700 font-mono">{{ perm.name }}</span>
                            </label>
                            <p v-if="permissions.length === 0" class="px-3 py-4 text-xs text-slate-400 text-center">
                                No permissions found. Run the seeder or open Permissions page.
                            </p>
                        </div>
                    </div>

                    <div v-if="formError" class="p-2.5 rounded-lg bg-red-50 text-red-600 text-sm">
                        {{ formError }}
                    </div>

                    <div class="flex justify-end gap-2 pt-2">
                        <button type="button" @click="closeModal"
                            class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg">
                            Cancel
                        </button>
                        <button type="submit" :disabled="saving"
                            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg">
                            {{ saving ? 'Saving...' : (editingRole ? 'Update' : 'Create') }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Delete -->
        <div v-if="deletingRole" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/40" @click="deletingRole = null" />
            <div class="relative w-full max-w-sm bg-white rounded-2xl shadow-xl p-6">
                <h3 class="text-lg font-semibold text-slate-800 mb-2">Delete Role</h3>
                <p class="text-sm text-slate-600 mb-5">
                    Delete <strong>{{ deletingRole.name }}</strong>? This cannot be undone.
                </p>
                <div class="flex justify-end gap-2">
                    <button type="button" @click="deletingRole = null"
                        class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg">
                        Cancel
                    </button>
                    <button type="button" @click="handleDelete" :disabled="saving"
                        class="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg">
                        {{ saving ? 'Deleting...' : 'Delete' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
    getRoles,
    createRole,
    updateRole,
    deleteRole,
    getPermissions,
} from '../../services/roles'
import type { Role, Permission } from '../../types/role'

const roles = ref<Role[]>([])
const permissions = ref<Permission[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const formError = ref('')
const showModal = ref(false)
const editingRole = ref<Role | null>(null)
const deletingRole = ref<Role | null>(null)

const form = reactive({
    name: '',
    description: '',
    permission_ids: [] as number[],
})

const resetForm = (): void => {
    form.name = ''
    form.description = ''
    form.permission_ids = []
    formError.value = ''
}

const parseDetail = (err: any): string => {
    const d = err.response?.data?.detail
    if (typeof d === 'string') return d
    if (d?.message) return d.message
    return 'Something went wrong'
}

const loadRoles = async (): Promise<void> => {
    loading.value = true
    error.value = ''
    try {
        roles.value = await getRoles()
    } catch (err: any) {
        error.value = parseDetail(err)
    } finally {
        loading.value = false
    }
}

const loadPermissions = async (): Promise<void> => {
    try {
        permissions.value = await getPermissions()
    } catch {
        permissions.value = []
    }
}

const selectAll = (): void => {
    form.permission_ids = permissions.value.map((p) => p.id)
}

const openCreate = (): void => {
    editingRole.value = null
    resetForm()
    showModal.value = true
}

const openEdit = (role: Role): void => {
    editingRole.value = role
    form.name = role.name
    form.description = role.description ?? ''
    form.permission_ids = permissions.value
        .filter((p) => role.permissions.includes(p.name))
        .map((p) => p.id)
    formError.value = ''
    showModal.value = true
}

const closeModal = (): void => {
    showModal.value = false
    editingRole.value = null
    resetForm()
}

const handleSubmit = async (): Promise<void> => {
    saving.value = true
    formError.value = ''
    try {
        if (editingRole.value) {
            await updateRole(editingRole.value.id, {
                name: form.name,
                description: form.description || null,
                permission_ids: form.permission_ids,
            })
        } else {
            await createRole({
                name: form.name,
                description: form.description || null,
                permission_ids: form.permission_ids,
            })
        }
        closeModal()
        await loadRoles()
    } catch (err: any) {
        formError.value = parseDetail(err)
    } finally {
        saving.value = false
    }
}

const confirmDelete = (role: Role): void => {
    if (role.name === 'ADMIN') return
    deletingRole.value = role
}

const handleDelete = async (): Promise<void> => {
    if (!deletingRole.value) return
    saving.value = true
    try {
        await deleteRole(deletingRole.value.id)
        deletingRole.value = null
        await loadRoles()
    } catch (err: any) {
        error.value = parseDetail(err)
        deletingRole.value = null
    } finally {
        saving.value = false
    }
}

onMounted(async () => {
    await Promise.all([loadRoles(), loadPermissions()])
})
</script>