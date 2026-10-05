<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-slate-800">Welcome back</h1>
        <p class="text-slate-500 mt-1">Sign in to your account</p>
      </div>

      <!-- Error message -->
      <div
        v-if="error"
        class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm border border-red-100"
      >
        {{ error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1.5">
            Email
          </label>
          <input
            v-model="form.email"
            type="email"
            required
            placeholder="you@example.com"
            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg text-sm
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   transition"
            :disabled="loading"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1.5">
            Password
          </label>
          <input
            v-model="form.password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg text-sm
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   transition"
            :disabled="loading"
          />
        </div>

        <!-- Remember + Forgot -->
        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              v-model="remember"
              type="checkbox"
              class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-slate-600">Remember me</span>
          </label>
          <a href="#" class="text-blue-600 hover:underline">Forgot password?</a>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400
                 text-white font-medium rounded-lg transition flex items-center justify-center gap-2"
        >
          <svg
            v-if="loading"
            class="animate-spin h-4 w-4 text-white"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
          </svg>
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/auth'
// import type { LoginPayload } from '@/services/auth'
import type { LoginPayload } from '@/services/auth'

const router = useRouter()

const form = reactive<LoginPayload>({
  email: '',
  password: '',
})

const remember = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async (): Promise<void> => {
  error.value = ''
  loading.value = true

  try {
    const data = await login(form)

    // Save token
    localStorage.setItem('token', data.access_token)

    if (data.user) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }

    // Redirect to dashboard
    await router.push('/')
  } catch (err: any) {
    // Handle Laravel / common API errors
    if (err.response?.data?.message) {
      error.value = err.response.data.message
    } else if (err.response?.data?.errors) {
      const errors = err.response.data.errors
      error.value = Object.values(errors).flat().join(' ')
    } else {
      error.value = 'Login failed. Please check your credentials.'
    }
  } finally {
    loading.value = false
  }
}
</script>