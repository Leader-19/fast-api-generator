import api from './api'
import type {
    Role,
    RoleCreate,
    RoleUpdate,
    RolePermissionAssign,
    Permission,
} from '@/types/role'

export const getRoles = async (): Promise<Role[]> => {
    const { data } = await api.get<Role[]>('roles')
    return data
}

export const getRole = async (id: number): Promise<Role> => {
    const { data } = await api.get<Role>(`roles/${id}`)
    return data
}

export const createRole = async (payload: RoleCreate): Promise<Role> => {
    const { data } = await api.post<Role>('roles', payload)
    return data
}

export const updateRole = async (id: number, payload: RoleUpdate): Promise<Role> => {
    const { data } = await api.put<Role>(`roles/${id}`, payload)
    return data
}

export const assignPermissions = async (
    id: number,
    payload: RolePermissionAssign,
): Promise<Role> => {
    const { data } = await api.post<Role>(`roles/${id}/permissions`, payload)
    return data
}

export const deleteRole = async (id: number): Promise<void> => {
    await api.delete(`roles/${id}`)
}

export const getPermissions = async (): Promise<Permission[]> => {
    const { data } = await api.get<Permission[]>('permissions')
    return data
}