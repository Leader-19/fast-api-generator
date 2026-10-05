export interface Permission {
  id: number
  name: string
  description?: string | null
}

export interface Role {
  id: number
  name: string
  description: string | null
  permissions: string[]
}

export interface RoleCreate {
  name: string
  description?: string | null
  permission_ids: number[]
}

export interface RoleUpdate {
  name?: string
  description?: string | null
  permission_ids?: number[]
}

export interface RolePermissionAssign {
  permission_ids: number[]
}