<template>
  <nav class="navigation">
    <div class="nav-container">
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>

        <!-- Customer Links -->
        <template v-if="!authStore.isAuthenticated.value || !authStore.isProvider.value">
          <router-link to="/customer/services" class="nav-link">Browse Services</router-link>
          <router-link to="/customer/orders" class="nav-link" v-if="authStore.isAuthenticated.value">My Orders</router-link>
        </template>

        <!-- Provider Links -->
        <template v-if="authStore.isAuthenticated.value && authStore.isProvider.value">
          <router-link to="/provider/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/provider/services" class="nav-link">My Services</router-link>
          <router-link to="/provider/orders" class="nav-link">Orders</router-link>
        </template>
      </div>

      <div class="nav-auth">
        <template v-if="authStore.isAuthenticated.value">
          <div class="user-info">
            <span class="user-avatar"></span>
            <span class="user-email">{{ authStore.user.value?.email }}</span>
            <div class="user-dropdown">
              <button @click="toggleDropdown" class="dropdown-toggle">
                ▼
              </button>
              <div v-if="showDropdown" class="dropdown-menu">
                <div class="dropdown-item user-details">
                  <strong>{{ authStore.userDisplayName.value }}</strong>
                  <span class="user-role">{{ authStore.isProvider.value ? 'Provider' : 'Customer' }}</span>
                </div>
                <button @click="handleLogout" class="dropdown-item logout-btn">
                  Logout
                </button>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleLogout = () => {
  authStore.logout()
  showDropdown.value = false
  router.push('/')
}

// Close dropdown when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.user-dropdown')) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Initialize auth state from localStorage
  authStore.initializeAuth()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.navigation {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
}

.nav-links {
  display: flex;
  gap: 0;
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  padding: 20px 30px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  border-bottom-color: #007bff;
  color: #007bff;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #333;
  position: relative;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ff6b35;
  display: inline-block;
}

.user-email {
  font-weight: 500;
  color: #333;
}

.user-dropdown {
  position: relative;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px;
  font-size: 12px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 1000;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 12px 16px;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.user-details {
  border-bottom: 1px solid #e0e0e0;
  cursor: default;
}

.user-details:hover {
  background-color: transparent;
}

.user-details strong {
  display: block;
  color: #333;
  margin-bottom: 4px;
}

.user-role {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logout-btn {
  color: #dc3545;
  font-weight: 500;
}

.logout-btn:hover {
  background-color: #f8f9fa;
  color: #c82333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 15px;
    height: 50px;
  }

  .nav-links {
    gap: 0;
  }

  .nav-link {
    padding: 15px 20px;
    font-size: 14px;
  }

  .user-email {
    display: none;
  }

  .dropdown-menu {
    min-width: 180px;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 10px;
  }

  .nav-link {
    padding: 15px 15px;
    font-size: 13px;
  }

  .nav-auth {
    gap: 10px;
  }
}
</style>