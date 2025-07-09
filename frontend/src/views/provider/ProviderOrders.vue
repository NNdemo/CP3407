<template>
  <div class="provider-orders">
    <div class="container">
      <div class="page-header">
        <h1>Order Management</h1>
        <p>Review and manage incoming booking requests</p>
      </div>

      <div class="orders-filters">
        <button
          v-for="filter in filters"
          :key="filter.value"
          @click="activeFilter = filter.value; loadOrders()"
          :class="['filter-btn', { active: activeFilter === filter.value }]"
        >
          {{ filter.label }}
          <span v-if="filter.count !== undefined" class="count-badge">{{ filter.count }}</span>
        </button>
      </div>

      <div class="orders-list">
        <div v-if="loading" class="loading">Loading orders...</div>
        <div v-else-if="orders.length === 0" class="no-orders">
          No orders found for the selected filter.
        </div>
        <div v-else>
          <div v-for="order in orders" :key="order.id" class="order-card">
            <div class="order-header">
              <div class="order-number">
                <h3>{{ order.order_number }}</h3>
                <span :class="['order-status', order.status]">{{ formatStatus(order.status) }}</span>
              </div>
              <div class="order-amount">
                ${{ order.total_price.toFixed(2) }}
              </div>
            </div>

            <div class="order-details">
              <div class="customer-info">
                <h4>Customer Information</h4>
                <p><strong>Name:</strong> {{ order.customer_name }}</p>
                <p><strong>Service:</strong> {{ order.service_type_name }}</p>
              </div>

              <div class="service-info">
                <h4>Service Details</h4>
                <p><strong>Date:</strong> {{ formatDate(order.service_date) }}</p>
                <p><strong>Time:</strong> {{ formatTime(order.service_time_start) }} - {{ formatTime(order.service_time_end) }}</p>
              </div>
            </div>

            <div class="order-actions">
              <template v-if="order.status === 'pending'">
                <button @click="updateOrderStatus(order, 'confirmed')" class="btn btn-success">
                  Accept Order
                </button>
                <button @click="updateOrderStatus(order, 'cancelled')" class="btn btn-danger">
                  Decline Order
                </button>
              </template>

              <template v-else-if="order.status === 'confirmed'">
                <button @click="updateOrderStatus(order, 'in_progress')" class="btn btn-primary">
                  Start Service
                </button>
                <button @click="updateOrderStatus(order, 'cancelled')" class="btn btn-secondary">
                  Cancel Order
                </button>
              </template>

              <template v-else-if="order.status === 'in_progress'">
                <button @click="updateOrderStatus(order, 'completed')" class="btn btn-success">
                  Complete Service
                </button>
              </template>

              <template v-else>
                <button @click="viewOrderDetails(order)" class="btn btn-secondary">
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
import { ordersAPI, type Order } from '../../services/api'

const orders = ref<Order[]>([])
const loading = ref(false)
const activeFilter = ref('all')

const filters = computed(() => [
  {
    label: 'All Orders',
    value: 'all',
    count: orders.value.length
  },
  {
    label: 'Pending',
    value: 'pending',
    count: orders.value.filter(o => o.status === 'pending').length
  },
  {
    label: 'Confirmed',
    value: 'confirmed',
    count: orders.value.filter(o => o.status === 'confirmed').length
  },
  {
    label: 'In Progress',
    value: 'in_progress',
    count: orders.value.filter(o => o.status === 'in_progress').length
  },
  {
    label: 'Completed',
    value: 'completed',
    count: orders.value.filter(o => o.status === 'completed').length
  }
])

const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': 'Pending Review',
    'confirmed': 'Confirmed',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'cancelled': 'Cancelled'
  }
  return statusMap[status] || status
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatTime = (timeString: string) => {
  const [hours, minutes] = timeString.split(':')
  const hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour % 12 || 12
  return `${displayHour}:${minutes} ${ampm}`
}

const loadOrders = async () => {
  loading.value = true
  try {
    const status = activeFilter.value === 'all' ? undefined : activeFilter.value
    orders.value = await ordersAPI.getOrders(status)
  } catch (error) {
    console.error('Error loading orders:', error)
  } finally {
    loading.value = false
  }
}

const updateOrderStatus = async (order: Order, newStatus: string) => {
  try {
    // In a real app, this would call an update API
    console.log(`Updating order ${order.order_number} status to ${newStatus}`)
    // await ordersAPI.updateOrderStatus(order.id, newStatus)

    // Update local state
    order.status = newStatus
  } catch (error) {
    console.error('Error updating order status:', error)
  }
}

const viewOrderDetails = (order: Order) => {
  // In a real app, this would navigate to order details page
  console.log('Viewing order details:', order)
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.provider-orders {
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

.orders-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-btn {
  background: white;
  border: 1px solid #ddd;
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.filter-btn:hover {
  border-color: #007bff;
  color: #007bff;
}

.filter-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.count-badge {
  background: rgba(0, 0, 0, 0.1);
  color: inherit;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: bold;
}

.filter-btn.active .count-badge {
  background: rgba(255, 255, 255, 0.2);
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.loading, .no-orders {
  text-align: center;
  color: #666;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.order-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
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

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.order-number h3 {
  color: #333;
  margin: 0 0 8px 0;
  font-size: 1.3rem;
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

.order-amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: #28a745;
}

.order-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 25px;
}

.customer-info h4, .service-info h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1rem;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
  display: inline-block;
}

.customer-info p, .service-info p {
  color: #666;
  margin: 5px 0;
  line-height: 1.5;
}

.customer-info strong, .service-info strong {
  color: #333;
}

.order-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  flex: 1;
  min-width: 120px;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

/* Responsive Design */
@media (max-width: 768px) {
  .provider-orders {
    padding: 15px;
  }

  .page-header {
    padding: 20px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .orders-filters {
    flex-direction: column;
  }

  .filter-btn {
    justify-content: center;
  }

  .order-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .order-details {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .order-actions {
    flex-direction: column;
  }

  .btn {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .order-card {
    padding: 20px;
  }

  .order-amount {
    font-size: 1.3rem;
  }
}
</style>