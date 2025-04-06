import { createRouter, createWebHashHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import CrearContrasenaView from '../views/CrearContrasenaView.vue'
import LoginView from '../views/LoginView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  {
    path: '/',
    name: 'Registration',
    component: RegistrationView
  },
  {
    path: '/crear-contrasena/:token',
    name: 'CrearContrasena',
    component: CrearContrasenaView,
    props: true
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Guard global para proteger la ruta /admin
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('adminAuthenticated')
    if (!isAuthenticated) {
      next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
