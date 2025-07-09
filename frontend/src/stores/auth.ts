import { ref, computed, reactive } from 'vue'
import { authAPI, type User } from '../services/api'

// Global reactive state
const authState = reactive({
  user: null as User | null,
  isLoading: false,
  error: null as string | null
})

// Computed properties
const isAuthenticated = computed(() => !!authState.user)
const isProvider = computed(() => authState.user?.is_provider || false)
const isCustomer = computed(() => !authState.user?.is_provider)
const userDisplayName = computed(() => {
  if (!authState.user) return ''
  return authState.user.first_name
    ? `${authState.user.first_name} ${authState.user.last_name || ''}`.trim()
    : authState.user.email
})

// Actions
const login = async (email: string, password: string) => {
  authState.isLoading = true
  authState.error = null

  try {
    const userData = await authAPI.login(email, password)
    authState.user = userData

    // Store user data in localStorage for persistence
    localStorage.setItem('user', JSON.stringify(userData))

    return userData
  } catch (err: any) {
    authState.error = err.message || 'Login failed'
    throw err
  } finally {
    authState.isLoading = false
  }
}

const register = async (userData: {
  email: string
  password: string
  phone?: string
  first_name?: string
  last_name?: string
}) => {
  authState.isLoading = true
  authState.error = null

  try {
    const newUser = await authAPI.register(userData)
    authState.user = newUser

    // Store user data in localStorage for persistence
    localStorage.setItem('user', JSON.stringify(newUser))

    return newUser
  } catch (err: any) {
    authState.error = err.message || 'Registration failed'
    throw err
  } finally {
    authState.isLoading = false
  }
}

const logout = () => {
  authState.user = null
  authState.error = null
  localStorage.removeItem('user')
}

const initializeAuth = () => {
  // Check if user data exists in localStorage
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      authState.user = JSON.parse(storedUser)
    } catch (err) {
      console.error('Failed to parse stored user data:', err)
      localStorage.removeItem('user')
    }
  }
}

const clearError = () => {
  authState.error = null
}

// Export the auth store as a composable
export const useAuthStore = () => {
  return {
    // State
    user: computed(() => authState.user),
    isLoading: computed(() => authState.isLoading),
    error: computed(() => authState.error),

    // Getters
    isAuthenticated,
    isProvider,
    isCustomer,
    userDisplayName,

    // Actions
    login,
    register,
    logout,
    initializeAuth,
    clearError
  }
}