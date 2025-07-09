<template>
  <div class="provider-services">
    <div class="container">
      <div class="page-header">
        <div class="header-content">
          <div>
            <h1>Service Management</h1>
            <p>Manage your service offerings, pricing, and availability</p>
          </div>
          <button @click="showAddModal = true" class="btn btn-primary">
            ➕ Add New Service
          </button>
        </div>
      </div>

      <div class="services-grid">
        <div v-if="loading" class="loading">Loading services...</div>
        <div v-else-if="services.length === 0" class="no-services">
          No services found.
        </div>
        <template v-else>
          <div v-for="service in services" :key="service.id" class="service-card">
            <!-- Service Header -->
            <div class="service-card-header">
              <div class="service-title-section">
                <h3 class="service-title">{{ service.name }}</h3>
                <span class="service-category-badge">{{ service.category_name }}</span>
              </div>
              <div class="service-status-indicator">
                <span :class="['status-badge', service.is_active ? 'active' : 'inactive']">
                  {{ service.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </div>

            <!-- Service Content -->
            <div class="service-card-body">
              <p class="service-description">{{ service.description || 'No description provided' }}</p>

              <!-- Service Metrics -->
              <div class="service-metrics">
                <div class="metric-item">
                  <span class="metric-label">Base Price</span>
                  <div class="metric-value price-value">
                    <span class="currency">$</span>
                    <span class="amount">{{ service.base_price }}</span>
                  </div>
                </div>
                <div class="metric-item">
                  <span class="metric-label">Duration</span>
                  <div class="metric-value">
                    <span class="duration">{{ service.duration_minutes || 60 }}</span>
                    <span class="unit">min</span>
                  </div>
                </div>
                <div class="metric-item">
                  <span class="metric-label">Status</span>
                  <div class="metric-value">
                    <span :class="['status-text', service.is_active ? 'active' : 'inactive']">
                      {{ service.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Quick Edit Controls -->
              <div class="quick-controls">
                <div class="control-group">
                  <label class="control-label">Price ($)</label>
                  <input
                    type="number"
                    v-model="service.base_price"
                    @change="updateService(service)"
                    class="control-input price-input"
                    step="0.01"
                    min="0"
                  >
                </div>
                <div class="control-group">
                  <label class="control-label">Duration (min)</label>
                  <input
                    type="number"
                    v-model="service.duration_minutes"
                    @change="updateService(service)"
                    class="control-input"
                    min="15"
                    step="15"
                  >
                </div>
              </div>

              <!-- Status Toggle -->
              <div class="status-control">
                <label class="toggle-switch">
                  <input
                    type="checkbox"
                    :checked="service.is_active"
                    @change="toggleAvailability(service)"
                  >
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">{{ service.is_active ? 'Service Active' : 'Service Inactive' }}</span>
                </label>
              </div>
            </div>

            <!-- Service Actions -->
            <div class="service-card-footer">
              <div class="action-buttons">
                <button @click="editService(service)" class="btn btn-primary btn-sm">
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                  Edit
                </button>
                <button @click="duplicateService(service)" class="btn btn-outline btn-sm">
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
                  Duplicate
                </button>
                <button @click="deleteService(service)" class="btn btn-danger btn-sm">
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <polyline points="3,6 5,6 21,6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                  Delete
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Add/Edit Service Modal -->
      <div v-if="showAddModal || editingService" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingService ? 'Edit Service' : 'Add New Service' }}</h2>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>

          <form @submit.prevent="saveService" class="edit-form">
            <div class="form-group">
              <label>Service Name:</label>
              <input
                type="text"
                v-model="currentService.name"
                required
                class="form-input"
                placeholder="Enter service name"
              >
            </div>

            <div class="form-group">
              <label>Category:</label>
              <select v-model="currentService.category_name" class="form-input" required>
                <option value="">Select Category</option>
                <option value="Flowers">Flowers</option>
                <option value="Cleaning">Cleaning</option>
                <option value="Gifts">Gifts</option>
              </select>
            </div>

            <div class="form-group">
              <label>Description:</label>
              <textarea
                v-model="currentService.description"
                rows="3"
                class="form-input"
                placeholder="Describe your service"
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Base Price ($):</label>
                <input
                  type="number"
                  v-model="currentService.base_price"
                  step="0.01"
                  min="0"
                  required
                  class="form-input"
                  placeholder="0.00"
                >
              </div>

              <div class="form-group">
                <label>Duration (minutes):</label>
                <input
                  type="number"
                  v-model="currentService.duration_minutes"
                  min="15"
                  step="15"
                  required
                  class="form-input"
                  placeholder="60"
                >
              </div>
            </div>

            <div class="form-group">
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="currentService.is_active"
                >
                <span class="checkmark"></span>
                Service is available for booking
              </label>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">
                {{ editingService ? 'Update Service' : 'Create Service' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { servicesAPI, type ServiceType } from '../../services/api'

const services = ref<ServiceType[]>([])
const loading = ref(false)
const editingService = ref<ServiceType | null>(null)
const showAddModal = ref(false)

// Current service being edited or created
const currentService = ref({
  id: 0,
  name: '',
  description: '',
  category_name: '',
  base_price: 0,
  duration_minutes: 60,
  is_active: true
})

const loadServices = async () => {
  loading.value = true
  try {
    // For demo, we'll use mock data with more services
    services.value = [
      { id: 1, name: 'Fresh Flowers', description: 'Beautiful fresh flower arrangements', category_name: 'Flowers', base_price: 21.00, is_active: true },
      { id: 2, name: 'Dried Flowers', description: 'Long-lasting dried flower arrangements', category_name: 'Flowers', base_price: 18.00, is_active: true },
      { id: 3, name: 'Designer Vase', description: 'Custom designed vases for special occasions', category_name: 'Gifts', base_price: 35.00, is_active: true },
      { id: 4, name: 'House Cleaning', description: 'Professional house cleaning service', category_name: 'Cleaning', base_price: 25.00, is_active: true },
      { id: 5, name: 'Office Cleaning', description: 'Commercial office cleaning service', category_name: 'Cleaning', base_price: 30.00, is_active: false },
      { id: 6, name: 'Aroma Candles', description: 'Premium scented candles for relaxation', category_name: 'Gifts', base_price: 15.00, is_active: true }
    ]
  } catch (error) {
    console.error('Error loading services:', error)
  } finally {
    loading.value = false
  }
}

const updateService = async (service: ServiceType) => {
  try {
    // In a real app, this would call an update API
    console.log('Updating service:', service)
    // await servicesAPI.updateService(service.id, service)
  } catch (error) {
    console.error('Error updating service:', error)
  }
}

const toggleAvailability = async (service: ServiceType) => {
  try {
    // In a real app, this would call an update API
    service.is_active = !service.is_active
    console.log('Toggling availability for service:', service)
    // await servicesAPI.updateService(service.id, { is_active: service.is_active })
  } catch (error) {
    console.error('Error toggling availability:', error)
  }
}

const editService = (service: ServiceType) => {
  editingService.value = { ...service }
  currentService.value = { ...service }
  showAddModal.value = false
}

const duplicateService = (service: ServiceType) => {
  currentService.value = {
    ...service,
    id: 0, // New service will get a new ID
    name: `${service.name} (Copy)`
  }
  editingService.value = null
  showAddModal.value = true
}

const deleteService = async (service: ServiceType) => {
  if (confirm(`Are you sure you want to delete "${service.name}"?`)) {
    try {
      // In a real app, this would call a delete API
      console.log('Deleting service:', service)
      // await servicesAPI.deleteService(service.id)

      // Remove from local array
      const index = services.value.findIndex(s => s.id === service.id)
      if (index !== -1) {
        services.value.splice(index, 1)
      }

      alert('Service deleted successfully!')
    } catch (error) {
      console.error('Error deleting service:', error)
      alert('Error deleting service. Please try again.')
    }
  }
}

const closeModal = () => {
  editingService.value = null
  showAddModal.value = false
  resetCurrentService()
}

const resetCurrentService = () => {
  currentService.value = {
    id: 0,
    name: '',
    description: '',
    category_name: '',
    base_price: 0,
    duration_minutes: 60,
    is_active: true
  }
}

const saveService = async () => {
  try {
    if (editingService.value) {
      // Update existing service
      console.log('Updating service:', currentService.value)
      // await servicesAPI.updateService(currentService.value.id, currentService.value)

      const index = services.value.findIndex(s => s.id === currentService.value.id)
      if (index !== -1) {
        services.value[index] = { ...currentService.value }
      }
      alert('Service updated successfully!')
    } else {
      // Create new service
      const newService = {
        ...currentService.value,
        id: Date.now() // Simple ID generation for demo
      }
      console.log('Creating service:', newService)
      // await servicesAPI.createService(newService)

      services.value.push(newService)
      alert('Service created successfully!')
    }

    closeModal()
  } catch (error) {
    console.error('Error saving service:', error)
    alert('Error saving service. Please try again.')
  }
}

onMounted(() => {
  loadServices()
})
</script>

<style scoped>
.provider-services {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.services-grid {
  display: grid;
  grid-template-columns: 1fr; /* Default single column */
  gap: 16px; /* Increased for better readability */
  width: 100%;
  margin-bottom: 40px;
}

/* 2-column layout for wide screens */
@media (min-width: 1920px) {
  .services-grid {
    grid-template-columns: 1fr 1fr; /* 2 columns on wide screens */
    gap: 24px;
  }
}

.loading, .no-services {
  grid-column: 1 / -1;
  text-align: center;
  color: #666;
  padding: 40px;
  background: white;
  border-radius: 8px;
}

.service-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e5e7eb;
  height: auto;
  min-height: 450px; /* Increased to prevent text truncation */
  display: flex;
  flex-direction: column;
  width: 100%; /* Full width within grid */
  overflow: visible; /* Allow content to be visible */
}

.service-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* Service Card Header */
.service-card-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.service-title-section {
  flex: 1;
}

.service-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.service-category-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.service-status-indicator {
  flex-shrink: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

/* Service Card Body */
.service-card-body {
  padding: 16px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.service-description {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
  min-height: auto; /* Remove fixed height to prevent truncation */
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Service Metrics */
.service-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.metric-item {
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.price-value {
  color: #059669;
}

.currency {
  font-size: 1rem;
  margin-right: 2px;
}

.unit {
  font-size: 0.9rem;
  color: #6b7280;
  margin-left: 2px;
}

.status-text.active {
  color: #059669;
}

.status-text.inactive {
  color: #dc2626;
}

/* Quick Controls */
.quick-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
}

.control-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

.control-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Status Control */
.status-control {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.toggle-switch {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.toggle-switch input {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 44px;
  height: 24px;
  background: #d1d5db;
  border-radius: 24px;
  transition: background 0.3s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.toggle-switch input:checked + .toggle-slider {
  background: #3b82f6;
}

.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

/* Service Card Footer */
.service-card-footer {
  padding: 16px 20px 20px;
  border-top: 1px solid #f3f4f6;
  margin-top: auto;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: space-between;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
}

.btn-icon {
  width: 14px;
  height: 14px;
}

.service-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.service-header h3 {
  color: #333;
  margin: 0;
}

.service-category {
  background: #e9ecef;
  color: #495057;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.service-description {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.5;
}

.service-pricing {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.price-info, .duration-info {
  display: flex;
  flex-direction: column;
}

.price-info label, .duration-info label {
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
  font-size: 14px;
}

.price-input {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.price-input span {
  background: #f8f9fa;
  padding: 8px 12px;
  color: #666;
  border-right: 1px solid #ddd;
}

.price-input input, .duration-info input {
  border: none;
  padding: 8px 12px;
  flex: 1;
  outline: none;
}

.duration-info input {
  border: 1px solid #ddd;
  border-radius: 4px;
}

.service-availability {
  margin-bottom: 20px;
}

.availability-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.availability-toggle input[type="checkbox"] {
  display: none;
}

.toggle-slider {
  width: 50px;
  height: 24px;
  background: #ccc;
  border-radius: 12px;
  position: relative;
  transition: background 0.3s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: white;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
}

.availability-toggle input:checked + .toggle-slider {
  background: #28a745;
}

.availability-toggle input:checked + .toggle-slider::before {
  transform: translateX(26px);
}

.toggle-label {
  font-weight: 500;
  color: #333;
}

.service-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  flex: 1;
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

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: 500;
  color: #333;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Modal Styles */
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
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-form {
  padding: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 25px;
}

/* Responsive Design */

@media (max-width: 768px) {
  .provider-services {
    padding: 8px;
  }

  .services-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .service-pricing {
    grid-template-columns: 1fr;
  }

  .service-actions {
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
  }
}
</style>