import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Viveiro from '@/views/Viveiro.vue'
import Login from '@/views/Login.vue'
import Usuarios from '@/views/Usuarios.vue'
import Replantios from '@/views/Replantios.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
      meta: { hideMenu: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/viveiro',
      name: 'viveiro',
      component: Viveiro
    },
    { path: '/usuarios', 
      name: 'usuarios', 
      component: Usuarios 
    },
    {
      path: '/replantios',
      name: 'replantios',
      component: Replantios
    },
  ],
})

// --- GUARDA DE ROTA ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  if (to.name !== 'login' && !isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
