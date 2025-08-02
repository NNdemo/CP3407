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

      <!-- Search Controls -->
      <div class="search-controls">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by order number, customer name, or service type..."
            class="search-input"
          >
          <span class="search-icon">🔍</span>
        </div>
      </div>

      <div class="orders-list">
        <div v-if="loading" class="loading">Loading orders...</div>
        <div v-else-if="filteredOrders.length === 0" class="no-orders">
          {{ orders.length === 0 ? 'No orders found for the selected filter.' : 'No orders match your search criteria.' }}
        </div>
        <div v-else>
          <div v-for="order in filteredOrders" :key="order.id" class="order-card">
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

    <!-- Order Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
      <div class="modal-content order-details-modal" @click.stop>
        <div class="modal-header">
          <h2>Order Details</h2>
          <button @click="closeDetailsModal" class="close-btn">&times;</button>
        </div>

        <div class="modal-body" v-if="selectedOrder">
          <div class="order-details-grid">
            <!-- Order Information -->
            <div class="details-section">
              <h3>Order Information</h3>
              <div class="detail-item">
                <label>Order Number:</label>
                <span>{{ selectedOrder.order_number }}</span>
              </div>
              <div class="detail-item">
                <label>Status:</label>
                <span class="status-badge" :class="selectedOrder.status">
                  {{ formatStatus(selectedOrder.status) }}
                </span>
              </div>
              <div class="detail-item">
                <label>Service Date:</label>
                <span>{{ formatDate(selectedOrder.service_date) }}</span>
              </div>
              <div class="detail-item">
                <label>Service Time:</label>
                <span>{{ selectedOrder.service_time_start }}</span>
              </div>
              <div class="detail-item">
                <label>Total Amount:</label>
                <span class="amount">${{ selectedOrder.total_price.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Customer Information -->
            <div class="details-section">
              <h3>Customer Information</h3>
              <div class="detail-item">
                <label>Name:</label>
                <span>{{ selectedOrder.customer_name }}</span>
              </div>
              <div class="detail-item">
                <label>Email:</label>
                <span>{{ selectedOrder.customer_email || 'Not provided' }}</span>
              </div>
              <div class="detail-item">
                <label>Phone:</label>
                <span>{{ selectedOrder.customer_phone || 'Not provided' }}</span>
              </div>
            </div>

            <!-- Service Information -->
            <div class="details-section">
              <h3>Service Information</h3>
              <div class="detail-item">
                <label>Service:</label>
                <span>{{ selectedOrder.service_name }}</span>
              </div>
              <div class="detail-item">
                <label>Duration:</label>
                <span>{{ selectedOrder.duration_minutes }} minutes</span>
              </div>
              <div class="detail-item">
                <label>Base Price:</label>
                <span>${{ selectedOrder.base_price?.toFixed(2) || 'N/A' }}</span>
              </div>
            </div>

            <!-- Additional Notes -->
            <div class="details-section full-width" v-if="selectedOrder.customer_notes">
              <h3>Customer Notes</h3>
              <div class="notes-content">
                {{ selectedOrder.customer_notes }}
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeDetailsModal" class="btn btn-secondary">
            Close
          </button>
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
const searchQuery = ref('')
const showDetailsModal = ref(false)
const selectedOrder = ref<Order | null>(null)

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

// Filtered orders computed property
const filteredOrders = computed(() => {
  let filtered = orders.value

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(order =>
      (order.order_number || '').toLowerCase().includes(query) ||
      (order.customer_name || '').toLowerCase().includes(query) ||
      (order.service_name || '').toLowerCase().includes(query)
    )
  }

  return filtered
})

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
    console.log(`Updating order ${order.order_number} status to ${newStatus}`)

    // Call the backend API to update order status
    await ordersAPI.updateOrderStatus(order.id, newStatus)

    // Update local state
    order.status = newStatus

    // Show success message
    alert(`Order ${order.order_number} status updated to ${newStatus}`)
  } catch (error) {
    console.error('Error updating order status:', error)
    alert('Failed to update order status. Please try again.')
  }
}

const viewOrderDetails = (order: Order) => {
  selectedOrder.value = order
  showDetailsModal.value = true
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedOrder.value = null
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

/* Search Controls */
.search-controls {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box {
  position: relative;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 16px;
}

/* Order Details Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.order-details-modal {
  background: white;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e1e5e9;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #f8f9fa;
}

.modal-body {
  padding: 24px;
}

.order-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.details-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.details-section.full-width {
  grid-column: 1 / -1;
}

.details-section h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
  border-bottom: 2px solid #007bff;
  padding-bottom: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #e1e5e9;
}

.detail-item:last-child {
  margin-bottom: 0;
  border-bottom: none;
}

.detail-item label {
  font-weight: 600;
  color: #555;
  margin-right: 12px;
}

.detail-item span {
  color: #333;
  text-align: right;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.confirmed {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.in_progress {
  background: #d4edda;
  color: #155724;
}

.status-badge.completed {
  background: #d1ecf1;
  color: #0c5460;
}

.amount {
  font-weight: 700;
  color: #28a745;
  font-size: 1.1rem;
}

.notes-content {
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 6px;
  padding: 16px;
  color: #333;
  line-height: 1.5;
  white-space: pre-wrap;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e1e5e9;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .order-details-grid {
    grid-template-columns: 1fr;
  }

  .modal-overlay {
    padding: 10px;
  }

  .order-details-modal {
    max-height: 95vh;
  }
}
</style>