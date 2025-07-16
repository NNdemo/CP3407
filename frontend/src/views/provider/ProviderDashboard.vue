<template>
  <div class="provider-dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>Provider Dashboard</h1>
        <p class="welcome-text">Welcome back, {{ authStore.userDisplayName.value }}!</p>
      </div>

      <div class="dashboard-stats">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-content">
            <h3>{{ stats.totalOrders }}</h3>
            <p>Total Orders</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <h3>{{ stats.pendingOrders }}</h3>
            <p>Pending Orders</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3>{{ stats.completedOrders }}</h3>
            <p>Completed Orders</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3>${{ stats.totalRevenue.toFixed(2) }}</h3>
            <p>Total Revenue</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">🛠️</div>
          <div class="stat-content">
            <h3>{{ stats.activeServices }}</h3>
            <p>Active Services</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-content">
            <h3>{{ stats.averageRating }}</h3>
            <p>Average Rating</p>
          </div>
        </div>
      </div>

      <div class="dashboard-actions">
        <router-link to="/provider/services" class="action-card">
          <div class="action-icon">🛠️</div>
          <h3>Manage Services</h3>
          <p>Update your service offerings, pricing, and availability</p>
        </router-link>

        <router-link to="/provider/orders" class="action-card">
          <div class="action-icon">📦</div>
          <h3>View Orders</h3>
          <p>Review and manage incoming booking requests</p>
        </router-link>
      </div>

      <div class="recent-orders">
        <h2>Recent Orders</h2>
        <div v-if="loading" class="loading">Loading recent orders...</div>
        <div v-else-if="recentOrders.length === 0" class="no-orders">
          No recent orders found.
        </div>
        <div v-else class="orders-list">
          <div v-for="order in recentOrders" :key="order.id" class="order-item">
            <div class="order-info">
              <h4>{{ order.order_number }}</h4>
              <p>{{ order.customer_name }}</p>
              <p>{{ order.service_type_name }}</p>
            </div>
            <div class="order-meta">
              <span class="order-date">{{ formatDate(order.service_date) }}</span>
              <span :class="['order-status', order.status]">{{ formatStatus(order.status) }}</span>
            </div>
            <div class="order-amount">
              ${{ order.total_price.toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { ordersAPI, servicesAPI, type Order, type ServiceType } from '../../services/api'

const authStore = useAuthStore()
const recentOrders = ref<Order[]>([])
const services = ref<ServiceType[]>([])
const loading = ref(false)

const stats = computed(() => {
  const totalOrders = recentOrders.value.length
  const pendingOrders = recentOrders.value.filter(o => o.status === 'pending').length
  const completedOrders = recentOrders.value.filter(o => o.status === 'completed').length
  const totalRevenue = recentOrders.value
    .filter(o => o.status === 'completed')
    .reduce((sum, order) => sum + order.total_price, 0)
  
  // New metrics
  const activeServices = services.value.filter(s => s.is_active).length
  const averageRating = services.value.length > 0 
    ? (services.value.reduce((sum, s) => sum + (s.rating || 0), 0) / services.value.length).toFixed(1)
    : '0.0'

  return {
    totalOrders,
    pendingOrders,
    completedOrders,
    totalRevenue,
    activeServices,
    averageRating
  }
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

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

const loadRecentOrders = async () => {
  loading.value = true
  try {
    // In a real app, this would be filtered by provider
    const orders = await ordersAPI.getOrders()
    recentOrders.value = orders.slice(0, 5) // Show only 5 recent orders
  } catch (error) {
    console.error('Error loading recent orders:', error)
  } finally {
    loading.value = false
  }
}

const loadServices = async () => {
  try {
    const servicesData = await servicesAPI.getServices()
    services.value = servicesData
  } catch (error) {
    console.error('Error loading services:', error)
  }
}

onMounted(() => {
  loadRecentOrders()
  loadServices()
})
</script>

<style scoped>
.provider-dashboard {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dashboard-header h1 {
  color: #333;
  margin-bottom: 10px;
  font-size: 2rem;
}

.welcome-text {
  color: #666;
  font-size: 1.1rem;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content h3 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 5px;
}

.stat-content p {
  color: #666;
  margin: 0;
}

.dashboard-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.action-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.action-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.action-card h3 {
  color: #333;
  margin-bottom: 10px;
}

.action-card p {
  color: #666;
  margin: 0;
}

.recent-orders {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.recent-orders h2 {
  color: #333;
  margin-bottom: 20px;
}

.loading, .no-orders {
  text-align: center;
  color: #666;
  padding: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.order-info h4 {
  color: #333;
  margin-bottom: 5px;
}

.order-info p {
  color: #666;
  margin: 2px 0;
  font-size: 14px;
}

.order-meta {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.order-date {
  font-size: 14px;
  color: #666;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.order-status.pending {
  background: #fff3cd;
  color: #856404;
}

.order-status.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.order-status.completed {
  background: #d4edda;
  color: #155724;
}

.order-amount {
  font-weight: bold;
  color: #333;
  font-size: 1.1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .provider-dashboard {
    padding: 15px;
  }

  .dashboard-header {
    padding: 20px;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .dashboard-stats {
    grid-template-columns: 1fr;
  }

  .dashboard-actions {
    grid-template-columns: 1fr;
  }

  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .order-meta {
    flex-direction: row;
    align-items: center;
  }
}
</style>