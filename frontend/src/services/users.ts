import api from './api'
import type { User, UserCreate, UserUpdate, Role } from '@/types/user'

export const getUsers = async (): Promise<User[]> => {
    const { data } = await api.get<User[]>('users')
    return data
}

export const getUser = async (id: number): Promise<User> => {
    const { data } = await api.get<User>(`users/${id}`)
    return data
}

export const createUser = async (payload: UserCreate): Promise<User> => {
    const { data } = await api.post<User>('users', payload)
    return data
}

export const updateUser = async (id: number, payload: UserUpdate): Promise<User> => {
    const { data } = await api.put<User>(`users/${id}`, payload)
    return data
}

export const deleteUser = async (id: number): Promise<void> => {
    await api.delete(`users/${id}`)
}

// Roles (for the dropdown)
export const getRoles = async (): Promise<Role[]> => {
    const { data } = await api.get<Role[]>('roles')
    return data
}