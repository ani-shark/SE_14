import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/SignIn',
    name: 'sign in',
    component: () => import(/* webpackChunkName: "sign in" */ '../views/SignInView.vue')
  },
  {
    path: '/Dashboard',
    name: 'student dashboard',
    component: () => import(/* webpackChunkName: "student dashboard" */ '../views/DashboardView.vue')
  },
  {
    path: '/Register',
    name: 'student registration',
    component: () => import(/* webpackChunkName: "student registration" */ '../views/RegistrationView.vue')
  },
  {
    path: '/Seek',
    name: 'seek portal',
    component: () => import(/* webpackChunkName: "seek portal" */ '../views/SeekPortalView.vue')
  },
  {
    path: '/Agent',
    name: 'AI Agent',
    component: () => import(/* webpackChunkName: "ai agent" */ '../views/AiAgentView.vue')
  },
  {
    path: '/Admin',
    name: 'Admin',
    component: () => import(/* webpackChunkName: "admin" */ '../views/AdminView.vue')
  },
  {
    path: '/Admin/SignIn',
    name: 'Admin Sign in',
    component: () => import(/* webpackChunkName: "admin sign in" */ '../views/AdminSignInView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
