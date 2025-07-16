import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'
import Services from '../views/Services.vue'
import Order from '../views/Order.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

// Provider components (lazy loaded)
const ProviderDashboard = () => import('../views/provider/ProviderDashboard.vue')
const ProviderServices = () => import('../views/provider/ProviderServices.vue')
const ProviderOrders = () => import('../views/provider/ProviderOrders.vue')

// Customer components (lazy loaded)
const CustomerServices = () => import('../views/customer/CustomerServices.vue')
const CustomerOrders = () => import('../views/customer/CustomerOrders.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },

    // Generic routes that redirect based on user role
    {
      path: '/services',
      name: 'services',
      // Use a dummy component for route definition
      component: Home,
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated.value) {
          next('/login')
        } else if (authStore.isProvider.value) {
          next('/provider/services')
        } else {
          next('/customer/services')
        }
      }
    },
    {
      path: '/order',
      name: 'order',
      component: Home, // Dummy component to satisfy RouteRecordRaw
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated.value) {
          next('/login')
        } else if (authStore.isProvider.value) {
          next('/provider/orders')
        } else {
          next('/customer/orders')
        }
      }
    },

    // Provider routes
    {
      path: '/provider',
      meta: { requiresAuth: true, requiresProvider: true },
      children: [
        {
          path: 'dashboard',
          name: 'provider-dashboard',
          component: ProviderDashboard
        },
        {
          path: 'services',
          name: 'provider-services',
          component: ProviderServices
        },
        {
          path: 'orders',
          name: 'provider-orders',
          component: ProviderOrders
        }
      ]
    },

    // Customer routes
    {
      path: '/customer',
      meta: { requiresAuth: true, requiresCustomer: true },
      children: [
        {
          path: 'services',
          name: 'customer-services',
          component: CustomerServices
        },
        {
          path: 'orders',
          name: 'customer-orders',
          component: CustomerOrders
        }
      ]
    },

    // Fallback routes
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Global navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth state if not already done
  if (!authStore.user.value) {
    authStore.initializeAuth()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated.value) {
    next('/login')
    return
  }

  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && authStore.isAuthenticated.value) {
    if (authStore.isProvider.value) {
      next('/provider/dashboard')
    } else {
      next('/customer/services')
    }
    return
  }

  // Check provider access
  if (to.meta.requiresProvider && !authStore.isProvider.value) {
    next('/customer/services')
    return
  }

  // Check customer access
  if (to.meta.requiresCustomer && authStore.isProvider.value) {
    next('/provider/dashboard')
    return
  }

  next()
})

export default router