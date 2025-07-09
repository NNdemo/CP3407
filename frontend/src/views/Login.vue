<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-form">
        <div class="logo">
          <div class="logo-icon"></div>
          <h1>MyClean</h1>
        </div>

        <form @submit.prevent="handleLogin">
          <div v-if="authStore.error.value" class="error-message">
            {{ authStore.error.value }}
          </div>

          <!-- Role Selection -->
          <div class="form-group">
            <div class="role-selection">
              <h3>Login as:</h3>
              <div class="role-buttons">
                <button
                  type="button"
                  @click="userRole = 'customer'"
                  :class="['role-btn', { active: userRole === 'customer' }]"
                >
                  👤 Customer
                </button>
                <button
                  type="button"
                  @click="userRole = 'provider'"
                  :class="['role-btn', { active: userRole === 'provider' }]"
                >
                  🏢 Service Provider
                </button>
              </div>
            </div>
          </div>

          <div class="form-group">
            <input
              type="email"
              v-model="email"
              placeholder="Email or phone number"
              class="form-input"
              required
              :disabled="authStore.isLoading.value"
            >
          </div>

          <div class="form-group">
            <input
              type="password"
              v-model="password"
              placeholder="Password"
              class="form-input"
              required
              :disabled="authStore.isLoading.value"
            >
          </div>

          <button type="submit" class="login-btn" :disabled="authStore.isLoading.value">
            {{ authStore.isLoading.value ? 'Logging in...' : `Login as ${userRole === 'customer' ? 'Customer' : 'Provider'}` }}
          </button>
        </form>

        <div class="form-footer">
          <p>Change to <router-link to="/register" class="link">Provider Login Page</router-link></p>
          <p>don't have account? <router-link to="/register" class="link">Register</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const userRole = ref<'customer' | 'provider'>('customer')

const handleLogin = async () => {
  try {
    // For demo purposes, we'll simulate login with role selection
    // In a real app, the role would be determined by the backend
    const mockUser = {
      id: 1,
      email: email.value,
      first_name: 'Demo',
      last_name: 'User',
      is_provider: userRole.value === 'provider',
      phone: '',
      created_at: new Date().toISOString()
    }

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Store user in auth state
    localStorage.setItem('user', JSON.stringify(mockUser))
    authStore.initializeAuth() // This will load the user from localStorage

    console.log('Login successful:', mockUser)

    // Redirect based on user role
    if (mockUser.is_provider) {
      router.push('/provider/dashboard')
    } else {
      router.push('/customer/services')
    }
  } catch (error) {
    console.error('Login error:', error)
    authStore.error.value = 'Login failed. Please try again.'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 8px;
  padding: 60px;
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.logo {
  margin-bottom: 40px;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: #2c5f5f;
  border-radius: 50%;
  margin: 0 auto 15px;
  position: relative;
}

.logo-icon::before {
  content: '🌿';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 24px;
}

.logo h1 {
  color: #2c5f5f;
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  text-align: center;
}

.form-input:focus {
  outline: none;
  border-color: #2c5f5f;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
  font-size: 14px;
}

.role-selection {
  text-align: center;
  margin-bottom: 20px;
}

.role-selection h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.role-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.role-btn {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #ddd;
  background: white;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 14px;
}

.role-btn:hover {
  border-color: #2c5f5f;
  color: #2c5f5f;
}

.role-btn.active {
  border-color: #2c5f5f;
  background: #2c5f5f;
  color: white;
}

.login-btn {
  width: 100%;
  padding: 15px;
  background: #333;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 30px;
  transition: background 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  background: #555;
}

.login-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.form-footer p {
  margin-bottom: 10px;
  color: #666;
}

.link {
  color: #5bc0de;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-container {
    padding: 40px 20px;
  }
}
</style>