<template>
  <div class="customer-orders">
    <div class="container">
      <div class="page-header">
        <h1>My Orders</h1>
        <p>Track your service bookings and history</p>
      </div>

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

        <router-link to="/customer/services" class="btn btn-primary">
          Book New Service
        </router-link>
      </div>

      <div class="orders-list">
        <div v-if="loading" class="loading">Loading orders...</div>

        <div v-else-if="orders.length === 0" class="no-orders">
          <div class="no-orders-icon">📋</div>
          <h3>No orders found</h3>
          <p>You haven't made any bookings yet.</p>
          <router-link to="/customer/services" class="btn btn-primary">
            Book Your First Service
          </router-link>
        </div>

        <div v-else>
          <div v-for="order in orders" :key="order.id" class="order-card">
            <div class="order-image">
              <div class="order-placeholder">
                {{ getServiceIcon(order.service_type_name) }}
              </div>
            </div>

            <div class="order-details">
              <div class="order-header">
                <h3>{{ order.order_number }}</h3>
                <span :class="['order-status', order.status]">{{ formatStatus(order.status) }}</span>
              </div>

              <div class="order-info">
                <div class="info-item">
                  <span class="label">Service:</span>
                  <span class="value">{{ order.service_type_name }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Date:</span>
                  <span class="value">{{ formatDate(order.service_date) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Time:</span>
                  <span class="value">{{ formatTime(order.service_time_start) }} - {{ formatTime(order.service_time_end) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Total:</span>
                  <span class="value price">${{ order.total_price.toFixed(2) }}</span>
                </div>
              </div>
            </div>

            <div class="order-actions">
              <template v-if="order.status === 'pending'">
                <button @click="cancelOrder(order)" class="btn btn-secondary">
                  Cancel Order
                </button>
              </template>

              <template v-else-if="order.status === 'completed'">
                <button @click="bookAgain(order)" class="btn btn-primary">
                  Book Again
                </button>
                <button @click="leaveReview(order)" class="btn btn-outline">
                  Leave Review
                </button>
              </template>

              <template v-else>
                <button @click="viewDetails(order)" class="btn btn-outline">
                  View Details
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { ordersAPI, type Order } from '../../services/api'

const router = useRouter()
const authStore = useAuthStore()

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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatTime = (timeString: string) => {
  const [hours, minutes] = timeString.split(':')
  const hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12
  return `${displayHour}:${minutes}${ampm.toLowerCase()}`
}

const getServiceIcon = (serviceName: string) => {
  if (serviceName.toLowerCase().includes('flower')) return '🌸'
  if (serviceName.toLowerCase().includes('clean')) return '🧹'
  if (serviceName.toLowerCase().includes('candle')) return '🕯️'
  if (serviceName.toLowerCase().includes('vase')) return '🏺'
  return '🛠️'
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
  // Navigate to services page with pre-selected service
  router.push('/customer/services')
}

const cancelOrder = async (order: Order) => {
  if (confirm('Are you sure you want to cancel this order?')) {
    try {
      // In a real app, this would call an API to cancel the order
      console.log('Cancelling order:', order.order_number)
      order.status = 'cancelled'
    } catch (error) {
      console.error('Error cancelling order:', error)
    }
  }
}

const viewDetails = (order: Order) => {
  // In a real app, this would navigate to order details page
  console.log('Viewing order details:', order)
}

const leaveReview = (order: Order) => {
  // In a real app, this would open a review modal or navigate to review page
  console.log('Leaving review for order:', order)
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.customer-orders {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 8px; /* Reduced from 20px */
}

.container {
  width: 100%; /* Remove max-width constraint */
  margin: 0 auto;
  padding: 0 8px; /* Add minimal padding */
}

/* Orders List Grid Layout */
.orders-list {
  display: grid;
  grid-template-columns: 1fr; /* Default single column */
  gap: 16px;
}

/* 2-column layout for wide screens */
@media (min-width: 1920px) {
  .orders-list {
    grid-template-columns: 1fr 1fr; /* 2 columns on wide screens */
    gap: 24px;
  }
}

.page-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.page-header h1 {
  color: #333;
  margin-bottom: 10px;
  font-size: 2rem;
}

.page-header p {
  color: #666;
  margin: 0;
}

.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-tabs {
  display: flex;
  flex: 1;
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
  font-weight: 500;
}

.tab:hover,
.tab.active {
  color: #5bc0de;
  border-bottom-color: #5bc0de;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  margin: 15px;
}

.btn-primary {
  background: #5bc0de;
  color: white;
}

.btn-primary:hover {
  background: #46b8da;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.no-orders {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.no-orders-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.no-orders h3 {
  color: #333;
  margin-bottom: 10px;
}

.no-orders p {
  color: #666;
  margin-bottom: 30px;
}

.order-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e5e7eb;
  margin-bottom: 16px;
  max-width: 100%;
  width: 100%;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.order-image {
  flex-shrink: 0;
}

.order-placeholder {
  width: 80px;
  height: 80px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  border: 2px solid #e9ecef;
}

.order-details {
  flex: 1;
}

.order-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.order-header h3 {
  color: #333;
  margin: 0;
  font-size: 1.2rem;
}

.order-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.order-status.pending {
  background: #fff3cd;
  color: #856404;
}

.order-status.confirmed {
  background: #d1ecf1;
  color: #0c5460;
}

.order-status.in_progress {
  background: #cce5ff;
  color: #004085;
}

.order-status.completed {
  background: #d4edda;
  color: #155724;
}

.order-status.cancelled {
  background: #f8d7da;
  color: #721c24;
}

.order-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item .label {
  color: #666;
  font-weight: 500;
}

.info-item .value {
  color: #333;
  font-weight: 500;
}

.info-item .value.price {
  color: #28a745;
  font-weight: bold;
  font-size: 1.1rem;
}

.order-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;
}

.order-actions .btn {
  margin: 0;
  min-width: 120px;
  font-size: 14px;
  padding: 8px 16px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .customer-orders {
    padding: 15px;
  }

  .page-header {
    padding: 20px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .orders-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tabs {
    order: 2;
  }

  .orders-header .btn {
    order: 1;
    margin: 15px 15px 0 15px;
  }

  .order-card {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .order-details {
    width: 100%;
  }

  .order-header {
    justify-content: center;
  }

  .order-info {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .order-actions {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .order-card {
    padding: 20px;
  }

  .order-placeholder {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .order-actions .btn {
    min-width: 100px;
    font-size: 13px;
  }
}
</style>