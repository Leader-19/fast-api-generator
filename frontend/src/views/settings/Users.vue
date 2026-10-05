<template>
    <div>
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div>
                <h2 class="text-2xl font-bold text-slate-800">Users</h2>
                <p class="text-sm text-slate-500 mt-1">Manage system users and roles</p>
            </div>
            <button type="button" @click="openCreate"
                class="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add User
            </button>
        </div>

        <!-- Error -->
        <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm border border-red-100">
            {{ error }}
        </div>

        <!-- Table -->
        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead class="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">ID</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Name</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Email</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Roles</th>
                            <th class="text-left px-4 py-3 font-medium text-slate-600">Status</th>
                            <th class="text-right px-4 py-3 font-medium text-slate-600">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-if="loading">
                            <td colspan="6" class="px-4 py-8 text-center text-slate-400">
                                Loading users...
                            </td>
                        </tr>
                        <tr v-else-if="users.length === 0">
                            <td colspan="6" class="px-4 py-8 text-center text-slate-400">
                                No users found
                            </td>
                        </tr>
                        <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50 transition">
                            <td class="px-4 py-3 text-slate-500">{{ user.id }}</td>
                            <td class="px-4 py-3 font-medium text-slate-800">{{ user.name }}</td>
                            <td class="px-4 py-3 text-slate-600">{{ user.email }}</td>
                            <td class="px-4 py-3">
                                <div class="flex flex-wrap gap-1">
                                    <span v-for="role in user.roles" :key="role"
                                        class="px-2 py-0.5 text-xs rounded-full bg-blue-50 text-blue-700">
                                        {{ role }}
                                    </span>
                                    <span v-if="user.roles.length === 0" class="text-slate-400 text-xs">—</span>
                                </div>
                            </td>
                            <td class="px-4 py-3">
                                <span class="px-2 py-0.5 text-xs rounded-full font-medium" :class="user.is_active
                                    ? 'bg-green-50 text-green-700'
                                    : 'bg-slate-100 text-slate-500'">
                                    {{ user.is_active ? 'Active' : 'Inactive' }}
                                </span>
                            </td>
                            <td class="px-4 py-3 text-right">
                                <div class="inline-flex items-center gap-1">
                                    <button type="button" @click="openEdit(user)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition"
                                        title="Edit">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button type="button" @click="confirmDelete(user)"
                                        class="p-1.5 rounded-lg text-slate-500 hover:text-red-600 hover:bg-red-50 transition"
                                        title="Delete">
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

        <!-- Create / Edit Modal -->
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/40" @click="closeModal" />
            <div class="relative w-full max-w-md bg-white rounded-2xl shadow-xl p-6">
                <h3 class="text-lg font-semibold text-slate-800 mb-4">
                    {{ editingUser ? 'Edit User' : 'Add User' }}
                </h3>

                <form @submit.prevent="handleSubmit" class="space-y-4">
                    <!-- Name -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Name</label>
                        <input v-model="form.name" type="text" required
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Full name" />
                    </div>

                    <!-- Email -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
                        <input v-model="form.email" type="email" required
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="user@example.com" />
                    </div>

                    <!-- Password -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">
                            Password
                            <span v-if="editingUser" class="text-slate-400 font-normal">(leave blank to keep)</span>
                        </label>
                        <input v-model="form.password" type="password" :required="!editingUser"
                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="••••••••" />
                    </div>

                    <!-- Roles -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Roles</label>
                        <div class="space-y-2 max-h-32 overflow-y-auto border border-slate-200 rounded-lg p-3">
                            <label v-for="role in roles" :key="role.id" class="flex items-center gap-2 cursor-pointer">
                                <input type="checkbox" :value="role.id" v-model="form.role_ids"
                                    class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                                <span class="text-sm text-slate-700">{{ role.name }}</span>
                            </label>
                            <p v-if="roles.length === 0" class="text-xs text-slate-400">No roles available</p>
                        </div>
                    </div>

                    <!-- Active -->
                    <label class="flex items-center gap-2 cursor-pointer">
                        <input v-model="form.is_active" type="checkbox"
                            class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                        <span class="text-sm text-slate-700">Active</span>
                    </label>

                    <!-- Form error -->
                    <div v-if="formError" class="p-2.5 rounded-lg bg-red-50 text-red-600 text-sm">
                        {{ formError }}
                    </div>

                    <!-- Actions -->
                    <div class="flex justify-end gap-2 pt-2">
                        <button type="button" @click="closeModal"
                            class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition">
                            Cancel
                        </button>
                        <button type="submit" :disabled="saving"
                            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg transition">
                            {{ saving ? 'Saving...' : (editingUser ? 'Update' : 'Create') }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Delete confirm -->
        <div v-if="deletingUser" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/40" @click="deletingUser = null" />
            <div class="relative w-full max-w-sm bg-white rounded-2xl shadow-xl p-6">
                <h3 class="text-lg font-semibold text-slate-800 mb-2">Delete User</h3>
                <p class="text-sm text-slate-600 mb-5">
                    Are you sure you want to delete
                    <strong>{{ deletingUser.name }}</strong>?
                    This action cannot be undone.
                </p>
                <div class="flex justify-end gap-2">
                    <button type="button" @click="deletingUser = null"
                        class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-lg transition">
                        Cancel
                    </button>
                    <button type="button" @click="handleDelete" :disabled="saving"
                        class="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-lg transition">
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
    getUsers,
    createUser,
    updateUser,
    deleteUser,
    getRoles,
} from '@/services/users'
import type { User, Role } from '@/types/user'

const users = ref<User[]>([])
const roles = ref<Role[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const formError = ref('')
const showModal = ref(false)
const editingUser = ref<User | null>(null)
const deletingUser = ref<User | null>(null)

const form = reactive({
    name: '',
    email: '',
    password: '',
    is_active: true,
    role_ids: [] as number[],
})

const resetForm = (): void => {
    form.name = ''
    form.email = ''
    form.password = ''
    form.is_active = true
    form.role_ids = []
    formError.value = ''
}

const loadUsers = async (): Promise<void> => {
    loading.value = true
    error.value = ''
    try {
        users.value = await getUsers()
    } catch (err: any) {
        error.value = err.response?.data?.detail ?? 'Failed to load users'
    } finally {
        loading.value = false
    }
}

const loadRoles = async (): Promise<void> => {
    try {
        roles.value = await getRoles()
    } catch {
        roles.value = []
    }
}

const openCreate = (): void => {
    editingUser.value = null
    resetForm()
    showModal.value = true
}

const openEdit = (user: User): void => {
    editingUser.value = user
    form.name = user.name
    form.email = user.email
    form.password = ''
    form.is_active = user.is_active
    // Map role names → ids
    form.role_ids = roles.value
        .filter((r) => user.roles.includes(r.name))
        .map((r) => r.id)
    formError.value = ''
    showModal.value = true
}

const closeModal = (): void => {
    showModal.value = false
    editingUser.value = null
    resetForm()
}

const handleSubmit = async (): Promise<void> => {
    saving.value = true
    formError.value = ''

    try {
        if (editingUser.value) {
            const payload: Record<string, unknown> = {
                name: form.name,
                email: form.email,
                is_active: form.is_active,
                role_ids: form.role_ids,
            }
            if (form.password) {
                payload.password = form.password
            }
            await updateUser(editingUser.value.id, payload)
        } else {
            await createUser({
                name: form.name,
                email: form.email,
                password: form.password,
                is_active: form.is_active,
                role_ids: form.role_ids,
            })
        }
        closeModal()
        await loadUsers()
    } catch (err: any) {
        formError.value =
            err.response?.data?.detail ??
            (typeof err.response?.data?.detail === 'string'
                ? err.response.data.detail
                : 'Something went wrong')
    } finally {
        saving.value = false
    }
}

const confirmDelete = (user: User): void => {
    deletingUser.value = user
}

const handleDelete = async (): Promise<void> => {
    if (!deletingUser.value) return
    saving.value = true
    try {
        await deleteUser(deletingUser.value.id)
        deletingUser.value = null
        await loadUsers()
    } catch (err: any) {
        error.value = err.response?.data?.detail ?? 'Failed to delete user'
        deletingUser.value = null
    } finally {
        saving.value = false
    }
}

onMounted(async () => {
    await Promise.all([loadUsers(), loadRoles()])
})
</script>