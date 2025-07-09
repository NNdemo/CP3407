<template>
  <div class="services">
    <div class="container">
      <div class="booking-form">
        <h1>Welcome to use our service. You can reserve a service here...</h1>

        <form @submit.prevent="submitBooking" class="form">
          <div class="form-group">
            <select v-model="selectedServiceType" @change="onServiceTypeChange" class="form-select">
              <option value="">Service Type ▼</option>
              <option v-for="service in services" :key="service.id" :value="service.id">
                {{ service.name }} - ${{ service.base_price }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <input
              type="date"
              v-model="selectedDate"
              class="form-input"
              placeholder="Date ▼"
            >
          </div>

          <div class="form-group">
            <select v-model="selectedDuration" class="form-select">
              <option value="">Duration ▼</option>
              <option v-for="duration in durations" :key="duration.id" :value="duration.id">
                {{ duration.duration_label }} - ${{ calculatePrice(duration) }}
              </option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="!canSubmit">
              Confirm Booking
            </button>
            <button type="button" class="btn btn-secondary" @click="resetForm">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { servicesAPI, ordersAPI, type ServiceType, type ServiceDuration } from '../services/api'

const router = useRouter()

const services = ref<ServiceType[]>([])
const durations = ref<ServiceDuration[]>([])
const selectedServiceType = ref<number | ''>('')
const selectedDate = ref('')
const selectedDuration = ref<number | ''>('')
const loading = ref(false)

const canSubmit = computed(() => {
  return selectedServiceType.value && selectedDate.value && selectedDuration.value
})

const selectedService = computed(() => {
  return services.value.find(s => s.id === selectedServiceType.value)
})

const calculatePrice = (duration: ServiceDuration) => {
  if (!selectedService.value) return 0
  return (selectedService.value.base_price * duration.price_multiplier).toFixed(2)
}

const onServiceTypeChange = async () => {
  if (selectedServiceType.value) {
    try {
      durations.value = await servicesAPI.getServiceDurations(selectedServiceType.value as number)
    } catch (error) {
      console.error('Error fetching durations:', error)
    }
  } else {
    durations.value = []
  }
  selectedDuration.value = ''
}

const submitBooking = async () => {
  if (!canSubmit.value) return

  loading.value = true
  try {
    const orderData = {
      service_type_id: selectedServiceType.value as number,
      service_duration_id: selectedDuration.value as number,
      service_date: selectedDate.value,
      service_time_start: '11:00:00', // Default time for demo
      customer_notes: ''
    }

    await ordersAPI.createOrder(orderData)
    alert('Booking confirmed successfully!')
    router.push('/order')
  } catch (error) {
    console.error('Error creating order:', error)
    alert('Error creating booking. Please try again.')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  selectedServiceType.value = ''
  selectedDate.value = ''
  selectedDuration.value = ''
  durations.value = []
}

onMounted(async () => {
  try {
    services.value = await servicesAPI.getServices()
  } catch (error) {
    console.error('Error fetching services:', error)
  }
})
</script>

<style scoped>
.services {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 60px 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.booking-form {
  background: white;
  padding: 60px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.booking-form h1 {
  color: #333;
  margin-bottom: 60px;
  font-size: 1.8rem;
  font-weight: 500;
}

.form {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 30px;
}

.form-select,
.form-input {
  width: 100%;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background: #f8f8f8;
  color: #666;
  text-align: center;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.form-actions {
  display: flex;
  gap: 20px;
  margin-top: 40px;
}

.btn {
  flex: 1;
  padding: 15px 30px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #5bc0de;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #46b8da;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #ccc;
  color: #666;
}

.btn-secondary:hover {
  background: #bbb;
}

@media (max-width: 768px) {
  .booking-form {
    padding: 40px 20px;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>