import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface User {
  id: number
  email: string
  phone?: string
  first_name?: string
  last_name?: string
  is_provider: boolean
}

export interface ServiceType {
  id: number
  name: string
  description?: string
  base_price: number
  duration_minutes?: number
  category_name: string
  is_active: boolean
  provider_name?: string
  rating?: number
  reviews_count?: number
  image_url?: string
}

export interface ServiceDuration {
  id: number
  service_type_id: number
  duration_minutes: number
  duration_label: string
  price_multiplier: number
}

export interface Order {
  id: number
  order_number: string
  customer_name: string
  service_date: string
  service_time_start: string
  service_time_end: string
  total_price: number
  status: string
  service_type_name: string
}

export interface OrderCreate {
  service_type_id: number
  service_duration_id: number
  service_date: string
  service_time_start: string
  customer_notes?: string
}

// Auth API
export const authAPI = {
  login: async (email: string, password: string): Promise<User> => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  register: async (userData: {
    email: string
    password: string
    phone?: string
    first_name?: string
    last_name?: string
  }): Promise<User> => {
    const response = await api.post('/auth/register', userData)
    return response.data
  }
}

// Services API
export const servicesAPI = {
  getServices: async (includeInactive: boolean = false): Promise<ServiceType[]> => {
    const params = includeInactive ? { include_inactive: true } : {}
    const response = await api.get('/services', { params })
    return response.data
  },

  getServiceDurations: async (serviceId: number): Promise<ServiceDuration[]> => {
    const response = await api.get(`/services/${serviceId}/durations`)
    return response.data
  },

  updateService: async (serviceId: number, serviceData: Partial<ServiceType>): Promise<{message: string, service_id: number}> => {
    const response = await api.put(`/services/${serviceId}`, serviceData)
    return response.data
  },

  createService: async (serviceData: {
    name: string
    description?: string
    category_name: string
    base_price: number
    duration_minutes?: number
    is_active?: boolean
  }): Promise<ServiceType> => {
    const response = await api.post('/services', serviceData)
    return response.data
  }
}

// Orders API
export const ordersAPI = {
  createOrder: async (orderData: OrderCreate): Promise<Order> => {
    const response = await api.post('/orders', orderData)
    return response.data
  },

  getOrders: async (status?: string): Promise<Order[]> => {
    const params = status ? { status } : {}
    const response = await api.get('/orders', { params })
    return response.data
  },

  getOrder: async (orderId: number): Promise<Order> => {
    const response = await api.get(`/orders/${orderId}`)
    return response.data
  },

  updateOrderStatus: async (orderId: number, status: string): Promise<{message: string, order_id: number, new_status: string}> => {
    const response = await api.put(`/orders/${orderId}/status?status=${status}`)
    return response.data
  }
}

export default api