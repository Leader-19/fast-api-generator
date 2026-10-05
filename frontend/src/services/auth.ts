import api from './api'

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type?: string
  user?: {
    id: number
    name: string
    email: string
  }
}

export const login = async (payload: LoginPayload): Promise<LoginResponse> => {
  // Final URL = baseURL + 'auth/login'
  // → http://127.0.0.1:8000/api/auth/login
  const { data } = await api.post<LoginResponse>('auth/login', payload)
  return data
}

export const logout = (): void => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export const getToken = (): string | null => {
  return localStorage.getItem('token')
}

export const isAuthenticated = (): boolean => {
  return !!getToken()
}