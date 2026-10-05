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
    meta: { guest: true },
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
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
      },

      {
        path: 'operations',
        children: [
          {
            path: '',
            name: 'Operations',
            component: () => import('@/views/operations/index.vue'),
          },
          {
            path: 'pdf',
            name: 'PDF',
            component: () => import('@/views/operations/PDF/PdfConverter.vue'),
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