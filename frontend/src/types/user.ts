export interface User {
  id: number
  name: string
  email: string
  is_active: boolean
  roles: string[]
}

export interface UserCreate {
  name: string
  email: string
  password: string
  is_active: boolean
  role_ids: number[]
}

export interface UserUpdate {
  name?: string
  email?: string
  password?: string
  is_active?: boolean
  role_ids?: number[]
}

export interface Role {
  id: number
  name: string
}