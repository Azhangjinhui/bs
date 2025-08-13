import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@/store'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/register/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/layout/index.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('../views/home/index.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/profile/index.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'password',
        name: 'Password',
        component: () => import('../views/password/index.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'data-table',
        name: 'DataTable',
        component: () => import('../views/dataTable/index.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'data-analysis',
        name: 'DataAnalysis',
        component: () => import('../views/dataAnalysis/index.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: '/screen',
    name: 'ScreenFull',
    component: () => import('../views/index/index.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  userStore.initApp()
  const isLoggedIn = userStore.isLoggedIn
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
