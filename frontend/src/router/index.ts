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
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
