<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-form">
        <div class="logo">
          <div class="logo-icon"></div>
          <h1>MyClean</h1>
        </div>

        <form @submit.prevent="handleRegister">
          <div v-if="authStore.error.value" class="error-message">
            {{ authStore.error.value }}
          </div>

          <!-- Role Selection -->
          <div class="form-group">
            <div class="role-selection">
              <h3>Register as:</h3>
              <div class="role-buttons">
                <button
                  type="button"
                  @click="userRole = 'customer'"
                  :class="['role-btn', { active: userRole === 'customer' }]"
                >
                  👤 Customer
                  <small>Book services</small>
                </button>
                <button
                  type="button"
                  @click="userRole = 'provider'"
                  :class="['role-btn', { active: userRole === 'provider' }]"
                >
                  🏢 Service Provider
                  <small>Offer services</small>
                </button>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <input
                type="text"
                v-model="firstName"
                placeholder="First Name"
                class="form-input"
                :disabled="authStore.isLoading.value"
              >
            </div>
            <div class="form-group">
              <input
                type="text"
                v-model="lastName"
                placeholder="Last Name"
                class="form-input"
                :disabled="authStore.isLoading.value"
              >
            </div>
          </div>

          <div class="form-group">
            <input
              type="email"
              v-model="email"
              placeholder="Email"
              class="form-input"
              required
              :disabled="authStore.isLoading.value"
            >
          </div>

          <div class="form-group">
            <input
              type="tel"
              v-model="phone"
              placeholder="Phone Number (optional)"
              class="form-input"
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

          <button type="submit" class="register-btn" :disabled="authStore.isLoading.value">
            {{ authStore.isLoading.value ? 'Registering...' : 'Register' }}
          </button>
        </form>

        <div class="form-footer">
          <p>Change to <router-link to="/login" class="link">Provider Login Page</router-link></p>
          <p>Already have account? <router-link to="/login" class="link">Login</router-link></p>
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
const firstName = ref('')
const lastName = ref('')
const phone = ref('')
const userRole = ref<'customer' | 'provider'>('customer')

const handleRegister = async () => {
  try {
    // Use the real registration from the auth store
    const userData = await authStore.register({
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      phone: phone.value
    })
    
    // Override the is_provider value based on user's role selection
    // This allows users to register and immediately access the role they want
    const userWithSelectedRole = {
      ...userData,
      is_provider: userRole.value === 'provider'
    }
    
    // Update the stored user data with the selected role
    localStorage.setItem('user', JSON.stringify(userWithSelectedRole))
    authStore.initializeAuth() // This will load the updated user from localStorage

    console.log('Registration successful:', userWithSelectedRole)

    // Redirect based on user's role selection
    if (userWithSelectedRole.is_provider) {
      router.push('/provider/dashboard')
    } else {
      router.push('/customer/services')
    }
  } catch (error) {
    console.error('Registration error:', error)
    // Error is already set in the auth store
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
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

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  flex: 1;
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
  margin-bottom: 25px;
}

.role-selection h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.role-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.role-btn {
  flex: 1;
  padding: 20px 15px;
  border: 2px solid #ddd;
  background: white;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.role-btn small {
  font-size: 12px;
  opacity: 0.8;
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

.register-btn {
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

.register-btn:hover:not(:disabled) {
  background: #555;
}

.register-btn:disabled {
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
  .register-container {
    padding: 40px 20px;
  }
}
</style>