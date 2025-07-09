<template>
  <div class="orders">
    <div class="container">
      <div class="orders-header">
        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="activeTab = tab.value; loadOrders()"
            :class="['tab', { active: activeTab === tab.value }]"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div class="orders-list">
        <div v-if="loading" class="loading">Loading orders...</div>

        <div v-else-if="orders.length === 0" class="no-orders">
          No orders found.
        </div>

        <div v-else>
          <div v-for="order in orders" :key="order.id" class="order-card">
            <div class="order-image">
              <div class="order-placeholder"></div>
            </div>

            <div class="order-details">
              <div class="order-info">
                <p><strong>Order Number:</strong> {{ order.order_number }}</p>
                <p><strong>Order State:</strong> {{ formatStatus(order.status) }}</p>
                <p><strong>Service Time:</strong> {{ formatTime(order.service_time_start) }} - {{ formatTime(order.service_time_end) }}</p>
              </div>
            </div>

            <div class="order-actions">
              <div class="order-price">
                <span class="price">${{ order.total_price.toFixed(2) }}</span>
              </div>
              <button class="btn btn-secondary" @click="bookAgain(order)">
                Booking Again
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ordersAPI, type Order } from '../services/api'

const router = useRouter()

const orders = ref<Order[]>([])
const loading = ref(false)
const activeTab = ref('all')

const tabs = [
  { label: 'All', value: 'all' },
  { label: 'Appointment in progress', value: 'in_progress' },
  { label: 'Completed orders', value: 'completed' }
]

const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': 'Pending',
    'confirmed': 'Confirmed',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'cancelled': 'Cancelled'
  }
  return statusMap[status] || status
}

const formatTime = (timeString: string) => {
  // Convert 24-hour format to 12-hour format
  const [hours, minutes] = timeString.split(':')
  const hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12
  return `${displayHour}:${minutes}${ampm.toLowerCase()}`
}

const loadOrders = async () => {
  loading.value = true
  try {
    const status = activeTab.value === 'all' ? undefined : activeTab.value
    orders.value = await ordersAPI.getOrders(status)
  } catch (error) {
    console.error('Error loading orders:', error)
  } finally {
    loading.value = false
  }
}

const bookAgain = (order: Order) => {
  // Navigate to services page to create a new booking
  router.push('/services')
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.orders {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.orders-header {
  background: white;
  padding: 0;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.filter-tabs {
  display: flex;
}

.tab {
  flex: 1;
  padding: 20px;
  border: none;
  background: white;
  color: #666;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab:hover,
.tab.active {
  color: #5bc0de;
  border-bottom-color: #5bc0de;
}

.orders-list {
  space-y: 20px;
}

.loading,
.no-orders {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
}

.order-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.order-image {
  flex-shrink: 0;
}

.order-placeholder {
  width: 80px;
  height: 80px;
  background: #ddd;
  border-radius: 4px;
}

.order-details {
  flex: 1;
}

.order-info p {
  margin-bottom: 8px;
  color: #333;
}

.order-info strong {
  color: #333;
}

.order-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 15px;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #ccc;
  color: #666;
}

.btn-secondary:hover {
  background: #bbb;
}

@media (max-width: 768px) {
  .order-card {
    flex-direction: column;
    text-align: center;
  }

  .order-actions {
    align-items: center;
  }

  .filter-tabs {
    flex-direction: column;
  }
}
</style>