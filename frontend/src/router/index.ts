// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import DefaultAppLayout from '@/layouts/DefaultAppLayout.vue'
import { isAuthenticated } from '@/services/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/auth/Login.vue'),
    meta: { guest: true, title: 'Sign in' },
  },

  {
    path: '/',
    component: DefaultAppLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: 'Dashboard' },
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
        meta: { title: 'Reconciliation Reports' },
      },
      {
        path: 'reports/runs/:runId',
        name: 'ReportRunDetail',
        component: () => import('@/views/reports/RunDetail.vue'),
        meta: { title: 'Run Details' },
      },

      {
        path: 'operations',
        children: [
          {
            path: '',
            name: 'Operations',
            component: () => import('@/views/operations/index.vue'),
            meta: { title: 'Operations' },
          },
          {
            path: 'pdf',
            name: 'PDF',
            component: () => import('@/views/operations/PDF/PdfConverter.vue'),
            meta: { title: 'PDF Converter' },
          }

        ]
         
      },
      // Settings parent
      {
        path: 'settings',
        children: [
          {
            path: '',
            name: 'Settings',
            component: () => import('@/views/settings/SettingsLayout.vue'),
          },
          {
            path: 'users',
            name: 'SettingsUsers',
            component: () => import('@/views/settings/Users.vue'),
          },
          {
            path: 'roles',
            name: 'SettingsRoles',
            component: () => import('@/views/settings/Roles.vue'),
          },
          {
            path: 'permissions',
            name: 'SettingsPermissions',
            component: () => import('@/views/settings/Permissions.vue'),
          },
        ],
      },
    ],
  },

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.afterEach((to) => {
  const title = to.meta.title as string | undefined

  document.title = title
    ? `${title} · Roaming Portal`
    : 'Roaming Portal'
})

router.beforeEach((to) => {
  const loggedIn = isAuthenticated()

  if (to.meta.requiresAuth && !loggedIn) {
    return { name: 'Login' }
  }

  if (to.meta.guest && loggedIn) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router