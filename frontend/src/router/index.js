import Dashboard from '@/views/Dashboard.vue'
import Viveiro from '@/views/Viveiro.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/viveiro',
      name: 'viveiro',
      component: Viveiro
    }
  ],
})

export default router
