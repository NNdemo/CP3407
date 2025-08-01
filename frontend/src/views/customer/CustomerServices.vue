<template>
  <div class="marketplace">
    <!-- Hero Section with Search -->
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Discover Premium Services</h1>
          <p class="hero-subtitle">Find the perfect service for your needs from trusted providers</p>

          <!-- Search Bar -->
          <div class="search-container">
            <div class="search-bar">
              <div class="search-input-wrapper">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                  v-model="searchQuery"
                  @input="debouncedSearch"
                  type="text"
                  placeholder="Search services, providers, or keywords..."
                  class="search-input"
                  aria-label="Search services"
                >
                <button
                  v-if="searchQuery"
                  @click="clearSearch"
                  class="clear-search"
                  aria-label="Clear search"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content - Full Width -->
    <div class="main-content">
      <div class="container">
        <!-- Unified Filter & Sort Control -->
        <div class="filter-sort-container">
        <!-- Main Control Bar -->
        <div class="control-bar">
          <div class="control-left">
            <button @click="toggleFilters" class="control-btn" :class="{ 'active': showFilters }">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
              </svg>
              <span>Filters</span>
              <span v-if="activeFiltersCount > 0" class="badge">{{ activeFiltersCount }}</span>
              <svg class="chevron" :class="{ 'rotated': showFilters }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </button>
          </div>

          <div class="control-center">
            <div class="sort-group">
              <label class="sort-label">Sort by:</label>
              <select v-model="sortBy" @change="applySorting" class="sort-select">
                <option value="name">Name (A-Z)</option>
                <option value="price-low">Price (Low to High)</option>
                <option value="price-high">Price (High to Low)</option>
                <option value="category">Category</option>
                <option value="availability">Availability</option>
              </select>
            </div>
          </div>

          <div class="control-right">
            <div class="results-info">
              <span class="results-text">{{ filteredServices.length }} of {{ services.length }} services</span>
            </div>
          </div>
        </div>

        <!-- Active Filters Bar -->
        <div v-if="hasActiveFilters" class="active-filters-bar">
          <div class="filter-tags">
            <span v-if="searchQuery" class="filter-tag search-tag">
              <svg class="tag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              "{{ searchQuery }}"
              <button @click="clearSearch" class="remove-btn">×</button>
            </span>
            <span v-if="selectedProvider" class="filter-tag provider-tag">
              <svg class="tag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              {{ selectedProvider }}
              <button @click="selectedProvider = ''; applyFilters(); updateURL()" class="remove-btn">×</button>
            </span>
            <span
              v-for="category in selectedCategories"
              :key="category"
              class="filter-tag category-tag"
            >
              <span class="tag-icon">{{ getCategoryIcon(category) }}</span>
              {{ category }}
              <button @click="toggleCategory(category)" class="remove-btn">×</button>
            </span>
            <span v-if="priceRange.min > 0 || priceRange.max < 999" class="filter-tag price-tag">
              <svg class="tag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
              ${{ priceRange.min }}-${{ priceRange.max }}
              <button @click="resetPriceRange" class="remove-btn">×</button>
            </span>
            <span v-if="filters.availableOnly" class="filter-tag availability-tag">
              <svg class="tag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
              Available only
              <button @click="filters.availableOnly = false; applyFilters()" class="remove-btn">×</button>
            </span>
          </div>
          <button @click="clearAllFilters" class="clear-all-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            Clear all
          </button>
        </div>

        <!-- Expandable Filters Panel -->
        <div v-show="showFilters" class="filters-panel">
          <div class="filters-content">
            <!-- Category Filters -->
            <div class="filter-section">
              <h4 class="filter-title">
                <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M4 6h16M4 12h16M4 18h7"></path>
                </svg>
                Categories
                <span v-if="selectedCategories.length > 0" class="count-badge">{{ selectedCategories.length }}</span>
              </h4>
              <div class="category-grid">
                <button
                  v-for="category in serviceCategories"
                  :key="category"
                  @click="toggleCategory(category)"
                  :class="['category-item', { active: selectedCategories.includes(category) }]"
                >
                  <span class="category-icon">{{ getCategoryIcon(category) }}</span>
                  <span class="category-name">{{ category }}</span>
                  <span v-if="selectedCategories.includes(category)" class="check-mark">✓</span>
                </button>
              </div>
            </div>

            <!-- Price Range Filter -->
            <div class="filter-section">
              <h4 class="filter-title">
                <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <line x1="12" y1="1" x2="12" y2="23"></line>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
                Price Range
              </h4>
              <div class="price-controls">
                <div class="price-inputs">
                  <div class="input-group">
                    <span class="input-prefix">$</span>
                    <input
                      v-model.number="priceRange.min"
                      @input="applyFilters"
                      type="number"
                      placeholder="0"
                      class="price-input"
                      min="0"
                      max="999"
                    >
                  </div>
                  <span class="range-separator">to</span>
                  <div class="input-group">
                    <span class="input-prefix">$</span>
                    <input
                      v-model.number="priceRange.max"
                      @input="applyFilters"
                      type="number"
                      placeholder="999"
                      class="price-input"
                      min="0"
                      max="999"
                    >
                  </div>
                </div>
                <div class="price-presets">
                  <button @click="setPriceRange(0, 50)" :class="['preset-btn', { active: priceRange.min === 0 && priceRange.max === 50 }]">
                    Under $50
                  </button>
                  <button @click="setPriceRange(50, 100)" :class="['preset-btn', { active: priceRange.min === 50 && priceRange.max === 100 }]">
                    $50-$100
                  </button>
                  <button @click="setPriceRange(100, 999)" :class="['preset-btn', { active: priceRange.min === 100 && priceRange.max === 999 }]">
                    $100+
                  </button>
                </div>
              </div>
            </div>

            <!-- Availability Filter -->
            <div class="filter-section">
              <h4 class="filter-title">
                <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12,6 12,12 16,14"></polyline>
                </svg>
                Availability
              </h4>
              <label class="toggle-control">
                <input
                  v-model="filters.availableOnly"
                  @change="applyFilters"
                  type="checkbox"
                  class="toggle-input"
                >
                <span class="toggle-slider"></span>
                <span class="toggle-label">Show available services only</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Services Grid -->
      <div class="services-section">
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading services...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredServices.length === 0" class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>No services found</h3>
          <p v-if="searchQuery">
            No services match your search for "<strong>{{ searchQuery }}</strong>"
          </p>
          <p v-else-if="hasActiveFilters">
            Try adjusting your filters to see more results
          </p>
          <p v-else>
            No services are currently available
          </p>
          <button
            v-if="hasActiveFilters || searchQuery"
            @click="clearAllFilters"
            class="btn btn-outline"
          >
            Clear filters
          </button>
        </div>

        <!-- Services Grid -->
        <div v-else class="services-grid">
          <div
            v-for="service in paginatedServices"
            :key="service.id"
            class="service-card"
            :class="{ 'unavailable': !service.is_active }"
          >
            <!-- Service Image/Icon -->
            <div class="service-image">
              <div class="service-icon">{{ getServiceIcon(service.category_name) }}</div>
              <div class="service-badge" :class="{ 'available': service.is_active, 'unavailable': !service.is_active }">
                {{ service.is_active ? 'Available' : 'Unavailable' }}
              </div>
              <button
                @click="toggleFavorite(service.id)"
                class="favorite-btn"
                :class="{ 'active': favorites.includes(service.id) }"
                :aria-label="favorites.includes(service.id) ? 'Remove from favorites' : 'Add to favorites'"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
              </button>
            </div>

            <!-- Service Content -->
            <div class="service-content">
              <div class="service-header">
                <h3 class="service-name">{{ service.name }}</h3>
                <span class="service-category">{{ service.category_name }}</span>
              </div>

              <p class="service-description">{{ service.description }}</p>

              <!-- Provider Info -->
              <div class="provider-info">
                <div class="provider-avatar">
                  <span>{{ getProviderInitials(service.provider_name || 'MyClean') }}</span>
                </div>
                <div class="provider-details">
                  <button
                    @click="filterByProvider(service.provider_name || 'MyClean')"
                    class="provider-name-btn"
                    :title="`View all services by ${service.provider_name || 'MyClean'}`"
                  >
                    {{ service.provider_name || 'MyClean' }}
                  </button>
                  <div class="provider-rating">
                    <div class="stars">
                      <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= (service.rating || 4.5) }">★</span>
                    </div>
                    <span class="rating-text">({{ service.rating || 4.5 }}) • {{ service.reviews_count || 12 }} reviews</span>
                  </div>
                </div>
              </div>

              <!-- Pricing -->
              <div class="service-pricing">
                <div class="price-main">
                  <span class="price-label">Starting from</span>
                  <span class="price-amount">${{ service.base_price }}</span>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="service-actions">
                <button
                  @click="quickBook(service)"
                  :disabled="!service.is_active"
                  class="btn btn-primary"
                  :class="{ 'disabled': !service.is_active }"
                >
                  {{ service.is_active ? 'Book Now' : 'Unavailable' }}
                </button>
                <button
                  @click="viewDetails(service)"
                  class="btn btn-outline"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="pagination-btn"
            aria-label="Previous page"
          >
            ‹
          </button>
          <span class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="pagination-btn"
            aria-label="Next page"
          >
            ›
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Booking Modal -->
    <div v-if="showBookingModal" class="modal-overlay" @click="closeBookingModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Book {{ selectedService?.name }}</h2>
          <button @click="closeBookingModal" class="modal-close" aria-label="Close modal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submitBooking" class="booking-form">
            <div class="form-group">
              <label for="booking-date" class="form-label">Select Date</label>
              <input
                id="booking-date"
                v-model="selectedDate"
                type="date"
                class="form-input"
                :min="minDate"
                required
              >
            </div>

            <div class="form-group">
              <label for="booking-duration" class="form-label">Duration</label>
              <select
                id="booking-duration"
                v-model="selectedDuration"
                class="form-select"
                required
              >
                <option value="">Select duration</option>
                <option v-for="duration in durations" :key="duration.id" :value="duration.id">
                  {{ duration.duration_label }} - ${{ calculatePrice(duration) }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="booking-notes" class="form-label">Special Instructions (Optional)</label>
              <textarea
                id="booking-notes"
                v-model="customerNotes"
                class="form-textarea"
                rows="3"
                placeholder="Any special requirements or notes..."
              ></textarea>
            </div>

            <div v-if="selectedService && selectedDurationObj" class="booking-summary">
              <h3>Booking Summary</h3>
              <div class="summary-item">
                <span>Service:</span>
                <span>{{ selectedService.name }}</span>
              </div>
              <div class="summary-item">
                <span>Date:</span>
                <span>{{ formatDate(selectedDate) }}</span>
              </div>
              <div class="summary-item">
                <span>Duration:</span>
                <span>{{ selectedDurationObj.duration_label }}</span>
              </div>
              <div class="summary-item total">
                <span>Total Price:</span>
                <span>${{ calculatePrice(selectedDurationObj) }}</span>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeBookingModal" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" :disabled="!canSubmit || loading" class="btn btn-primary">
                {{ loading ? 'Booking...' : 'Confirm Booking' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { servicesAPI, ordersAPI, type ServiceType, type ServiceDuration } from '../../services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Core data
const services = ref<ServiceType[]>([])
const durations = ref<ServiceDuration[]>([])
const loading = ref(false)

// Search and filters
const searchQuery = ref('')
const selectedCategories = ref<string[]>([])
const selectedProvider = ref('')
const priceRange = ref({ min: 0, max: 999 })
const filters = ref({
  availableOnly: false
})
const sortBy = ref('name')

// Pagination
const currentPage = ref(1)
const itemsPerPage = 12

// Booking modal
const showBookingModal = ref(false)
const selectedService = ref<ServiceType | null>(null)
const selectedDate = ref('')
const selectedDuration = ref<number | ''>('')
const customerNotes = ref('')

// Favorites
const favorites = ref<number[]>([])

// UI State
const showFilters = ref(false)

// Debounced search
let searchTimeout: number

const serviceCategories = computed(() => {
  const categories = [...new Set(services.value.map(s => s.category_name))]
  return categories.sort()
})

const hasActiveFilters = computed(() => {
  return selectedCategories.value.length > 0 ||
         selectedProvider.value.length > 0 ||
         priceRange.value.min > 0 ||
         priceRange.value.max < 999 ||
         filters.value.availableOnly ||
         searchQuery.value.length > 0
})

const activeFiltersCount = computed(() => {
  let count = 0
  if (searchQuery.value) count++
  if (selectedProvider.value) count++
  if (selectedCategories.value.length > 0) count += selectedCategories.value.length
  if (priceRange.value.min > 0 || priceRange.value.max < 999) count++
  if (filters.value.availableOnly) count++
  return count
})

const filteredServices = computed(() => {
  let filtered = [...services.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(service =>
      service.name.toLowerCase().includes(query) ||
      (service.description && service.description.toLowerCase().includes(query)) ||
      service.category_name.toLowerCase().includes(query) ||
      (service.provider_name && service.provider_name.toLowerCase().includes(query))
    )
  }

  // Category filter
  if (selectedCategories.value.length > 0) {
    filtered = filtered.filter(service =>
      selectedCategories.value.includes(service.category_name)
    )
  }

  // Provider filter
  if (selectedProvider.value) {
    filtered = filtered.filter(service =>
      service.provider_name === selectedProvider.value
    )
  }

  // Price range filter
  filtered = filtered.filter(service =>
    service.base_price >= priceRange.value.min &&
    service.base_price <= priceRange.value.max
  )

  // Availability filter
  if (filters.value.availableOnly) {
    filtered = filtered.filter(service => service.is_active)
  }

  return filtered
})

const sortedServices = computed(() => {
  const sorted = [...filteredServices.value]

  switch (sortBy.value) {
    case 'name':
      return sorted.sort((a, b) => a.name.localeCompare(b.name))
    case 'price-low':
      return sorted.sort((a, b) => a.base_price - b.base_price)
    case 'price-high':
      return sorted.sort((a, b) => b.base_price - a.base_price)
    case 'category':
      return sorted.sort((a, b) => a.category_name.localeCompare(b.category_name))
    case 'availability':
      return sorted.sort((a, b) => Number(b.is_active) - Number(a.is_active))
    default:
      return sorted
  }
})

const totalPages = computed(() => {
  return Math.ceil(sortedServices.value.length / itemsPerPage)
})

const paginatedServices = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return sortedServices.value.slice(start, end)
})

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const canSubmit = computed(() => {
  return selectedService.value && selectedDate.value && selectedDuration.value
})

const selectedDurationObj = computed(() => {
  return durations.value.find(d => d.id === selectedDuration.value)
})

// Methods
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
    updateURL()
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  applyFilters()
  updateURL()
}

const toggleCategory = (category: string) => {
  const index = selectedCategories.value.indexOf(category)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(category)
  }
  applyFilters()
  updateURL()
}

const applyFilters = () => {
  currentPage.value = 1
  nextTick(() => {
    // Trigger reactivity
  })
}

const applySorting = () => {
  currentPage.value = 1
  updateURL()
}

const clearAllFilters = () => {
  searchQuery.value = ''
  selectedCategories.value = []
  selectedProvider.value = ''
  priceRange.value = { min: 0, max: 999 }
  filters.value.availableOnly = false
  sortBy.value = 'name'
  currentPage.value = 1
  updateURL()
}

const updateURL = () => {
  const query: any = {}

  if (searchQuery.value) query.search = searchQuery.value
  if (selectedCategories.value.length > 0) query.categories = selectedCategories.value.join(',')
  if (priceRange.value.min > 0) query.minPrice = priceRange.value.min
  if (priceRange.value.max < 999) query.maxPrice = priceRange.value.max
  if (filters.value.availableOnly) query.available = 'true'
  if (sortBy.value !== 'name') query.sort = sortBy.value
  if (currentPage.value > 1) query.page = currentPage.value

  router.replace({ query })
}

const loadFromURL = () => {
  const query = route.query

  if (query.search) searchQuery.value = query.search as string
  if (query.categories) selectedCategories.value = (query.categories as string).split(',')
  if (query.minPrice) priceRange.value.min = Number(query.minPrice)
  if (query.maxPrice) priceRange.value.max = Number(query.maxPrice)
  if (query.available) filters.value.availableOnly = query.available === 'true'
  if (query.sort) sortBy.value = query.sort as string
  if (query.page) currentPage.value = Number(query.page)
}

const toggleFavorite = (serviceId: number) => {
  const index = favorites.value.indexOf(serviceId)
  if (index > -1) {
    favorites.value.splice(index, 1)
  } else {
    favorites.value.push(serviceId)
  }
  // Save to localStorage
  localStorage.setItem('service-favorites', JSON.stringify(favorites.value))
}

const loadFavorites = () => {
  const saved = localStorage.getItem('service-favorites')
  if (saved) {
    favorites.value = JSON.parse(saved)
  }
}

const resetPriceRange = () => {
  priceRange.value = { min: 0, max: 999 }
  applyFilters()
  updateURL()
}

const setPriceRange = (min: number, max: number) => {
  priceRange.value = { min, max }
  applyFilters()
  updateURL()
}

const filterByProvider = (providerName: string) => {
  selectedProvider.value = providerName
  // Clear other filters to focus on this provider
  searchQuery.value = ''
  selectedCategories.value = []
  applyFilters()
  updateURL()

  // Scroll to top to show results
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const toggleFilters = () => {
  showFilters.value = !showFilters.value
}

const quickBook = (service: ServiceType) => {
  if (!service.is_active) return
  selectedService.value = service
  showBookingModal.value = true
  loadDurations(service.id)
}

const viewDetails = (service: ServiceType) => {
  // Navigate to service details page or show details modal
  router.push(`/customer/services/${service.id}`)
}

const closeBookingModal = () => {
  showBookingModal.value = false
  selectedService.value = null
  selectedDate.value = ''
  selectedDuration.value = ''
  customerNotes.value = ''
  durations.value = []
}

const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    'Flowers': '🌸',
    'Cleaning': '🧹',
    'Gifts': '🎁'
  }
  return icons[category] || '🛠️'
}

const getProviderInitials = (name: string) => {
  return name.split(' ').map(word => word[0]).join('').toUpperCase().slice(0, 2)
}

const loadServices = async () => {
  loading.value = true
  try {
    // Use real API call instead of mock data
    const apiServices = await servicesAPI.getServices()
    
    // Transform the API response to match your frontend expectations
    services.value = apiServices.map(service => ({
      ...service,
      // Add default values for fields that don't exist in backend
      is_active: true, // Backend only returns active services
      provider_name: 'MyClean Services', // Default provider name
      rating: 4.5, // Default rating
      reviews_count: 10, // Default review count
      image_url: undefined // No images in backend
    }))
  } catch (error) {
    console.error('Error loading services:', error)
    // Fallback to mock data if API fails
    services.value = [
      {
        id: 1,
        name: 'Premium Flower Arrangement',
        description: 'Beautiful handcrafted flower arrangements for special occasions with fresh seasonal blooms',
        category_name: 'Flowers',
        base_price: 45.00,
        is_active: true,
        provider_name: 'Bloom & Blossom',
        rating: 4.8,
        reviews_count: 24
      },
      {
        id: 2,
        name: 'Wedding Bouquet Design',
        description: 'Custom wedding bouquets designed to match your special day theme and color palette',
        category_name: 'Flowers',
        base_price: 85.00,
        is_active: true,
        provider_name: 'Elegant Florals',
        rating: 4.9,
        reviews_count: 18
      },
      {
        id: 3,
        name: 'Deep House Cleaning',
        description: 'Comprehensive deep cleaning service including all rooms, appliances, and hard-to-reach areas',
        category_name: 'Cleaning',
        base_price: 120.00,
        is_active: true,
        provider_name: 'Sparkle Clean Co.',
        rating: 4.7,
        reviews_count: 45
      },
      {
        id: 4,
        name: 'Regular House Cleaning',
        description: 'Weekly or bi-weekly house cleaning service to keep your home spotless and organized',
        category_name: 'Cleaning',
        base_price: 75.00,
        is_active: true,
        provider_name: 'Fresh Home Services',
        rating: 4.6,
        reviews_count: 32
      },
      {
        id: 5,
        name: 'Office Cleaning Service',
        description: 'Professional office cleaning for businesses, including sanitization and waste management',
        category_name: 'Cleaning',
        base_price: 95.00,
        is_active: false,
        provider_name: 'Pro Clean Solutions',
        rating: 4.5,
        reviews_count: 28
      },
      {
        id: 6,
        name: 'Luxury Scented Candles',
        description: 'Hand-poured premium candles with natural wax and essential oils for relaxation',
        category_name: 'Gifts',
        base_price: 35.00,
        is_active: true,
        provider_name: 'Artisan Candle Co.',
        rating: 4.4,
        reviews_count: 15
      },
      {
        id: 7,
        name: 'Custom Gift Baskets',
        description: 'Personalized gift baskets with gourmet treats, wines, and artisanal products',
        category_name: 'Gifts',
        base_price: 65.00,
        is_active: true,
        provider_name: 'Gourmet Gifts',
        rating: 4.7,
        reviews_count: 22
      },
      {
        id: 8,
        name: 'Dried Flower Arrangements',
        description: 'Long-lasting dried flower arrangements perfect for home decoration and events',
        category_name: 'Flowers',
        base_price: 28.00,
        is_active: true,
        provider_name: 'Rustic Blooms',
        rating: 4.3,
        reviews_count: 19
      }
    ]
  } finally {
    loading.value = false
  }
}

const loadDurations = async (serviceId: number) => {
  try {
    // Use real API call
    durations.value = await servicesAPI.getServiceDurations(serviceId)
  } catch (error) {
    console.error('Error loading durations:', error)
    // Fallback to mock data
    durations.value = [
      { id: 1, service_type_id: serviceId, duration_minutes: 60, duration_label: '1 Hour', price_multiplier: 1.0 },
      { id: 2, service_type_id: serviceId, duration_minutes: 120, duration_label: '2 Hours', price_multiplier: 1.8 },
      { id: 3, service_type_id: serviceId, duration_minutes: 180, duration_label: '3 Hours', price_multiplier: 2.5 }
    ]
  }
}

const calculatePrice = (duration: ServiceDuration) => {
  if (!selectedService.value) return '0.00'
  return (selectedService.value.base_price * duration.price_multiplier).toFixed(2)
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getServiceIcon = (category: string) => {
  const icons: Record<string, string> = {
    'Flowers': '🌸',
    'Cleaning': '🧹',
    'Gifts': '🎁'
  }
  return icons[category] || '🛠️'
}



const submitBooking = async () => {
  if (!canSubmit.value) return

  loading.value = true
  try {
    const orderData = {
      service_type_id: selectedService.value?.id as number,
      service_duration_id: selectedDuration.value as number,
      service_date: selectedDate.value,
      service_time_start: '11:00:00', // Default time for demo
      customer_notes: customerNotes.value
    }

    console.log('Creating order with data:', orderData)

    // Use real API call instead of mock
    const createdOrder = await ordersAPI.createOrder(orderData)
    
    console.log('Order created:', createdOrder)

    // Show success message
    alert(`Booking confirmed! Order number: ${createdOrder.order_number}`)
    closeBookingModal()

    // Optionally redirect to orders page
    // router.push('/customer/orders')
  } catch (error) {
    console.error('Error creating order:', error)
    alert('Error creating booking. Please try again.')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  selectedDate.value = ''
  selectedDuration.value = ''
  customerNotes.value = ''
  durations.value = []
}

// Watchers
watch(() => route.query, () => {
  loadFromURL()
}, { immediate: true })

watch([selectedCategories, priceRange, filters], () => {
  applyFilters()
}, { deep: true })

// Lifecycle hooks
onMounted(async () => {
  await loadServices()
  loadFavorites()
  loadFromURL()
})
</script>

<style scoped>
/* Marketplace Styles */
.marketplace {
  min-height: 100vh;
  background: #f8fafc;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 0;
  margin-bottom: 40px;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

/* Search Bar */
.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-bar {
  position: relative;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #6b7280;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  background: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.clear-search {
  position: absolute;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-search:hover {
  background: #e5e7eb;
}

.clear-search svg {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

/* Container */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Unified Filter & Sort Container */
.filter-sort-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 24px;
  overflow: hidden;
}

/* Main Control Bar */
.control-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  background: #fafbfc;
}

.control-left {
  flex: 0 0 auto;
}

.control-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.control-right {
  flex: 0 0 auto;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.control-btn:hover {
  border-color: #3b82f6;
  background: #f0f9ff;
  color: #1e40af;
}

.control-btn.active {
  border-color: #3b82f6;
  background: #3b82f6;
  color: white;
}

.control-btn .icon {
  width: 18px;
  height: 18px;
}

.control-btn .badge {
  background: #ef4444;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.control-btn.active .badge {
  background: rgba(255,255,255,0.9);
  color: #3b82f6;
}

.control-btn .chevron {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.control-btn .chevron.rotated {
  transform: rotate(180deg);
}

.sort-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sort-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
  white-space: nowrap;
}

.sort-select {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
  cursor: pointer;
  min-width: 160px;
  transition: border-color 0.2s ease;
}

.sort-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.results-info {
  display: flex;
  align-items: center;
}

.results-text {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

/* Active Filters Bar */
.active-filters-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  gap: 16px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  flex: 1;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.filter-tag.search-tag {
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.filter-tag.provider-tag {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #6ee7b7;
}

.filter-tag.category-tag {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.filter-tag.price-tag {
  background: #e0e7ff;
  color: #3730a3;
  border: 1px solid #a5b4fc;
}

.filter-tag.availability-tag {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}

.filter-tag .tag-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.filter-tag .remove-btn {
  background: none;
  border: none;
  color: currentColor;
  cursor: pointer;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0;
  margin-left: 4px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.filter-tag .remove-btn:hover {
  background: rgba(0,0,0,0.1);
}

.clear-all-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #ef4444;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
  flex-shrink: 0;
}

.clear-all-btn:hover {
  background: #dc2626;
}

.clear-all-btn svg {
  width: 14px;
  height: 14px;
}

/* Expandable Filters Panel */
.filters-panel {
  background: white;
  border-top: 1px solid #e5e7eb;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.filters-panel:has(.filters-content) {
  max-height: 600px;
}

.filters-content {
  padding: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.filter-title .title-icon {
  width: 18px;
  height: 18px;
  color: #3b82f6;
}

.filter-title .count-badge {
  background: #3b82f6;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Category Grid */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 8px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.category-item:hover {
  border-color: #3b82f6;
  background: #f0f9ff;
  transform: translateY(-1px);
}

.category-item.active {
  border-color: #3b82f6;
  background: #3b82f6;
  color: white;
}

.category-item .category-icon {
  font-size: 1.5rem;
}

.category-item .category-name {
  font-size: 0.85rem;
  font-weight: 500;
  text-align: center;
}

.category-item .check-mark {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #10b981;
  color: white;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

/* Price Controls */
.price-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  transition: border-color 0.2s ease;
}

.input-group:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.input-prefix {
  padding: 0 8px;
  color: #6b7280;
  font-weight: 500;
  background: #f9fafb;
  border-right: 1px solid #e5e7eb;
}

.price-input {
  border: none;
  padding: 8px 12px;
  font-size: 0.9rem;
  background: transparent;
  flex: 1;
  min-width: 0;
}

.price-input:focus {
  outline: none;
}

.range-separator {
  color: #6b7280;
  font-weight: 500;
  font-size: 0.9rem;
}

.price-presets {
  display: flex;
  gap: 8px;
}

.preset-btn {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.preset-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Toggle Control */
.toggle-control {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.toggle-control:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.toggle-input {
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

.toggle-input:checked + .toggle-slider {
  background: #3b82f6;
}

.toggle-input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.filter-toggle-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.filter-icon {
  width: 18px;
  height: 18px;
  color: #3b82f6;
}

.filter-badge {
  background: #3b82f6;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chevron-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
  transition: transform 0.2s ease;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.sort-controls-compact {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
}

.sort-select-compact {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
  cursor: pointer;
  min-width: 120px;
}

.results-info-compact {
  font-size: 0.9rem;
  color: #6b7280;
}

/* Active Filters Compact */
.active-filters-compact {
  padding: 12px 20px;
  background: #f8fafc;
  border-top: 1px solid #e5e7eb;
}

.filter-tags-compact {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.filter-tag-compact {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #3b82f6;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.filter-tag-compact.provider-tag {
  background: #10b981;
}

.remove-tag-compact {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0;
  margin-left: 2px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.remove-tag-compact:hover {
  background: rgba(255,255,255,0.2);
}

.clear-all-compact {
  background: #ef4444;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.clear-all-compact:hover {
  background: #dc2626;
}

/* Collapsible Filters Panel */
.filters-panel {
  background: white;
  border-top: 1px solid #e5e7eb;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.filters-panel.expanded {
  max-height: 500px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.filter-group-compact {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-label-compact {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}

/* Compact Category Filters */
.category-filters-compact {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-btn-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  font-weight: 500;
}

.category-btn-compact:hover {
  border-color: #3b82f6;
  background: #f0f9ff;
}

.category-btn-compact.active {
  border-color: #3b82f6;
  background: #3b82f6;
  color: white;
}

/* Compact Price Filter */
.price-filter-compact {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-inputs-compact {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-input-compact {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  max-width: 80px;
}

.price-presets-compact {
  display: flex;
  gap: 6px;
}

.preset-btn-compact {
  flex: 1;
  padding: 4px 8px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn-compact:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.preset-btn-compact.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Compact Toggle */
.toggle-label-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.toggle-input-compact {
  display: none;
}

.toggle-slider-compact {
  position: relative;
  width: 36px;
  height: 20px;
  background: #d1d5db;
  border-radius: 20px;
  transition: background 0.3s ease;
}

.toggle-slider-compact::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.toggle-input-compact:checked + .toggle-slider-compact {
  background: #3b82f6;
}

.toggle-input-compact:checked + .toggle-slider-compact::before {
  transform: translateX(16px);
}

.toggle-text-compact {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
}

/* Filters Section */
.filters-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
}

.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.filter-icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.clear-all-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #fee2e2;
  color: #dc2626;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-all-btn:hover {
  background: #fecaca;
  transform: scale(1.1);
}

.clear-all-btn svg {
  width: 16px;
  height: 16px;
}

/* Active Filters */
.active-filters {
  background: #f0f9ff;
  border: 1px solid #0ea5e9;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.active-filters-header {
  margin-bottom: 12px;
}

.active-count {
  font-size: 0.9rem;
  font-weight: 600;
  color: #0369a1;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #3b82f6;
  color: white;
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 500;
}

.remove-tag {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0;
  margin-left: 4px;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.remove-tag:hover {
  background: rgba(255,255,255,0.2);
}

.filter-group {
  margin-bottom: 32px;
}

.filter-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.selected-count {
  font-size: 0.8rem;
  color: #3b82f6;
  font-weight: 600;
  background: #eff6ff;
  padding: 2px 8px;
  border-radius: 12px;
}

/* Category Filters */
.category-filters {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  text-align: left;
  position: relative;
}

.category-btn:hover {
  border-color: #d1d5db;
  background: #f9fafb;
  transform: translateY(-1px);
}

.category-btn.active {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #1d4ed8;
  box-shadow: 0 2px 4px rgba(59,130,246,0.2);
}

.category-btn .category-icon {
  font-size: 1.2rem;
}

.category-btn .category-name {
  flex: 1;
  margin-left: 12px;
}

.category-btn .check-icon {
  color: #10b981;
  font-weight: bold;
  font-size: 1.1rem;
}

/* Price Filter Enhancements */
.price-input-group {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  transition: border-color 0.2s ease;
}

.price-input-group:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.currency {
  padding: 0 8px;
  color: #6b7280;
  font-weight: 500;
  background: #f9fafb;
  border-right: 1px solid #e5e7eb;
}

.price-input {
  border: none;
  padding: 10px 12px;
  font-size: 0.95rem;
  background: transparent;
  flex: 1;
}

.price-input:focus {
  outline: none;
}

.price-separator {
  color: #6b7280;
  font-weight: 500;
  margin: 0 8px;
}

.price-presets {
  display: flex;
  gap: 6px;
  margin-top: 12px;
}

.preset-btn {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.preset-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Toggle Switch for Availability */
.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.toggle-label:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.toggle-input {
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

.toggle-input:checked + .toggle-slider {
  background: #3b82f6;
}

.toggle-input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-text {
  font-weight: 500;
  color: #374151;
}

/* Filter Summary */
.filter-summary {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-top: 24px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-label {
  font-size: 0.9rem;
  color: #6b7280;
}

.summary-value {
  font-weight: 600;
  color: #1f2937;
}

/* Provider Name Button */
.provider-name-btn {
  background: none;
  border: none;
  color: #3b82f6;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  text-decoration-color: transparent;
  transition: all 0.2s ease;
  padding: 0;
  font-size: inherit;
}

.provider-name-btn:hover {
  color: #1d4ed8;
  text-decoration-color: currentColor;
}
/* Price Filter */
.price-filter {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 12px;
}

.price-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
}

.price-separator {
  color: #6b7280;
  font-weight: 500;
}

.price-range-display {
  font-size: 0.9rem;
  color: #6b7280;
  text-align: center;
  padding: 8px;
  background: #f3f4f6;
  border-radius: 6px;
}

/* Checkbox Styles */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-weight: 500;
  color: #374151;
}

.checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.clear-filters-btn {
  width: 100%;
  padding: 12px;
  border: 2px solid #ef4444;
  background: white;
  color: #ef4444;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background: #ef4444;
  color: white;
}

/* Sort Section */
.sort-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 20px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sort-label {
  font-weight: 600;
  color: #374151;
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 0.95rem;
  cursor: pointer;
}

.results-info {
  color: #6b7280;
  font-weight: 500;
}

.results-count {
  font-size: 0.95rem;
}

.form-select:focus,
.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #007bff;
  background: white;
  color: #333;
}

.booking-summary {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 20px;
  margin: 25px 0;
  text-align: left;
}

.booking-summary h3 {
  color: #333;
  margin-bottom: 15px;
  text-align: center;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #e9ecef;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item.total {
  font-weight: bold;
  font-size: 1.1rem;
  color: #28a745;
  margin-top: 10px;
  padding-top: 15px;
  border-top: 2px solid #28a745;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 15px 30px;
  border: none;
  border-radius: 6px;
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
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
  padding: 10px 20px;
  font-size: 14px;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.services-showcase {
  margin-top: 60px;
}

.services-showcase h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2rem;
}

.services-filter {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid #ddd;
  background: white;
  color: #666;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.filter-btn:hover {
  border-color: #007bff;
  color: #007bff;
}

.filter-btn.active {
  border-color: #007bff;
  background: #007bff;
  color: white;
}

.loading, .no-services {
  text-align: center;
  color: #666;
  padding: 40px;
  font-size: 1.1rem;
}

.services-grid {
  display: grid;
  gap: 16px; /* Increased gap for better spacing */
  margin-bottom: 40px;
  justify-content: start; /* Changed from center to start for left alignment */
  width: 100%;

  /* Base: Larger minimum width to prevent circular element distortion */
  grid-template-columns: repeat(auto-fit, minmax(300px, 350px));
}

.service-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  border: 2px solid transparent;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #007bff;
}

.service-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  background: #d4edda;
  color: #155724;
}

.service-badge.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.service-details {
  margin: 15px 0;
}

.service-category {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 5px;
}

.service-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.service-card h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.service-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.service-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #28a745;
  margin-bottom: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }

  .booking-form {
    padding: 25px 20px;
  }

  .booking-form h1 {
    font-size: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }

  .service-card {
    padding: 25px;
  }
}

@media (max-width: 480px) {
  .booking-form {
    padding: 20px 15px;
  }

  .form-select,
  .form-input,
  .form-textarea {
    padding: 12px 15px;
    font-size: 16px; /* Prevents zoom on iOS */
  }

  .btn {
    padding: 12px 20px;
  }
}

/* Services Grid - Optimized for Circular Elements */
.services-grid {
  display: grid;
  gap: 16px; /* Increased gap for better spacing */
  margin-bottom: 40px;
  justify-content: start; /* Changed from center to start for left alignment */
  width: 100%;

  /* Base: Larger minimum width to prevent circular element distortion */
  grid-template-columns: repeat(auto-fit, minmax(300px, 350px));
}

/* Full-Width Container System - Minimal Padding */
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 1px; /* Minimal padding to move content even further left */
}

/* Responsive Grid - Limited to 4 Columns Maximum */
@media (min-width: 3440px) {
  .services-grid {
    grid-template-columns: repeat(4, 1fr); /* Fixed 4 columns on ultra-wide */
    gap: 24px;
    max-width: 1600px; /* Limit total width */
    margin: 0 auto 40px;
  }
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 2560px) and (max-width: 3439px) {
  .services-grid {
    grid-template-columns: repeat(4, 1fr); /* 4 columns */
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto 40px;
  }
  .container {
    padding: 0 20px;
  }
}

@media (min-width: 1920px) and (max-width: 2559px) {
  .services-grid {
    grid-template-columns: repeat(3, 1fr); /* 3 columns */
    gap: 18px;
    max-width: 1200px;
    margin: 0 auto 40px;
  }
  .container {
    padding: 0 16px;
  }
}

@media (min-width: 1440px) and (max-width: 1919px) {
  .services-grid {
    grid-template-columns: repeat(auto-fit, minmax(230px, 270px));
    gap: 12px;
  }
  .container {
    padding: 0 1px; /* Minimal padding to move content even further left */
  }
}

@media (min-width: 1024px) and (max-width: 1439px) {
  .services-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 260px));
    gap: 12px;
  }
  .container {
    padding: 0 1px; /* Minimal padding to move content even further left */
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .services-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
  }
  .container {
    padding: 0 12px; /* Reduced from 20px */
  }
}

@media (max-width: 767px) {
  .services-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  .container {
    padding: 0 8px; /* Reduced from 16px */
  }
}

/* Service Card */
.service-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  min-height: 420px; /* Increased for better proportions */
  height: auto; /* Allow dynamic height */
  width: 100%;
  min-width: 300px; /* Minimum width to prevent circular element distortion */
  max-width: 350px; /* Increased maximum width */
  margin: 0 auto; /* Center cards */
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
  border-color: #3b82f6;
}

.service-card.unavailable {
  opacity: 0.7;
}

.service-card.unavailable:hover {
  transform: none;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* Service Image */
.service-image {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-icon {
  font-size: 4rem;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.service-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.service-badge.available {
  background: #10b981;
  color: white;
}

.service-badge.unavailable {
  background: #ef4444;
  color: white;
}

.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
}

.favorite-btn.active {
  background: #ef4444;
  color: white;
}

.favorite-btn svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

/* Service Content */
.service-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1; /* Fill remaining space */
  justify-content: space-between;
}

.service-header {
  margin-bottom: 16px;
}

.service-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
  line-height: 1.3;
}

.service-category {
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

.service-description {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

/* Provider Info */
.provider-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.provider-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
}

.provider-details {
  flex: 1;
}

.provider-name {
  font-weight: 600;
  color: #1f2937;
  display: block;
  margin-bottom: 4px;
}

.provider-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #d1d5db;
  font-size: 0.9rem;
}

.star.filled {
  color: #fbbf24;
}

.rating-text {
  font-size: 0.8rem;
  color: #6b7280;
}

/* Service Pricing */
.service-pricing {
  margin-bottom: 24px;
}

.price-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 12px;
  border: 2px solid #0ea5e9;
}

.price-label {
  font-size: 0.8rem;
  color: #0369a1;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.price-amount {
  font-size: 2rem;
  font-weight: 800;
  color: #0c4a6e;
}

/* Service Actions */
.service-actions {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-primary:hover:not(.disabled) {
  background: #2563eb;
  border-color: #2563eb;
  transform: translateY(-1px);
}

.btn-outline {
  background: white;
  color: #3b82f6;
  border-color: #3b82f6;
}

.btn-outline:hover {
  background: #3b82f6;
  color: white;
}

.btn.disabled {
  background: #9ca3af;
  color: white;
  border-color: #9ca3af;
  cursor: not-allowed;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 40px;
  padding: 20px;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.2rem;
  font-weight: 600;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 500;
  color: #6b7280;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0,0,0,0.25);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 0;
  margin-bottom: 24px;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.modal-close {
  width: 40px;
  height: 40px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #e5e7eb;
}

.modal-close svg {
  width: 20px;
  height: 20px;
  color: #6b7280;
}

.modal-body {
  padding: 0 24px 24px;
}

.booking-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  border-color: #6b7280;
}

.btn-secondary:hover {
  background: #4b5563;
  border-color: #4b5563;
}

/* Enhanced Responsive Design */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .control-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .control-left,
  .control-center,
  .control-right {
    flex: none;
  }

  .sort-group {
    justify-content: space-between;
  }

  .results-info {
    justify-content: center;
  }

  .active-filters-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .filter-tags {
    justify-content: center;
  }

  .filters-content {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 20px;
  }

  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 32px 0;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .container {
    padding: 0 12px;
  }

  .filter-sort-container {
    margin: 0 -8px;
    border-radius: 0;
  }

  .control-bar {
    padding: 12px 16px;
  }

  .control-btn {
    font-size: 0.9rem;
    padding: 6px 12px;
  }

  .sort-group {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }

  .sort-select {
    width: 100%;
    min-width: auto;
  }

  .results-text {
    font-size: 0.85rem;
    text-align: center;
  }

  .active-filters-bar {
    padding: 10px 16px;
  }

  .filter-tags {
    gap: 6px;
    justify-content: flex-start;
  }

  .filter-tag {
    font-size: 0.75rem;
    padding: 3px 8px;
  }

  .clear-all-btn {
    font-size: 0.75rem;
    padding: 4px 8px;
  }

  .filters-content {
    padding: 16px;
    gap: 20px;
  }

  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 6px;
  }

  .category-item {
    padding: 8px 4px;
  }

  .category-item .category-icon {
    font-size: 1.2rem;
  }

  .category-item .category-name {
    font-size: 0.8rem;
  }

  .price-inputs {
    gap: 8px;
  }

  .price-input {
    font-size: 0.85rem;
    padding: 6px 8px;
  }

  .price-presets {
    gap: 6px;
  }

  .preset-btn {
    font-size: 0.8rem;
    padding: 6px 8px;
  }

  .service-card {
    border-radius: 12px;
  }

  .service-image {
    height: 140px;
  }

  .service-icon {
    font-size: 2.5rem;
  }

  .service-content {
    padding: 16px;
  }

  .service-actions {
    flex-direction: column;
    gap: 8px;
  }

  .provider-info {
    padding: 10px;
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .provider-rating {
    justify-content: center;
  }

  .modal-content {
    margin: 8px;
    border-radius: 12px;
  }

  .modal-header,
  .modal-body {
    padding-left: 16px;
    padding-right: 16px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.75rem;
  }

  .search-input {
    padding: 12px 12px 12px 40px;
    font-size: 0.95rem;
  }

  .search-icon {
    left: 12px;
    width: 18px;
    height: 18px;
  }

  .compact-filter-bar {
    margin: 0 -12px;
  }

  .filter-toggle-section {
    padding: 10px 12px;
    flex-direction: column;
    gap: 10px;
  }

  .filter-toggle-btn {
    font-size: 0.85rem;
    padding: 6px 10px;
  }

  .filter-badge {
    font-size: 0.7rem;
    padding: 1px 4px;
    min-width: 16px;
    height: 16px;
  }

  .sort-controls-compact {
    gap: 6px;
  }

  .sort-select-compact {
    font-size: 0.85rem;
    padding: 4px 8px;
  }

  .results-info-compact {
    font-size: 0.8rem;
  }

  .active-filters-compact {
    padding: 8px 12px;
  }

  .filter-tag-compact {
    font-size: 0.7rem;
    padding: 2px 5px;
  }

  .clear-all-compact {
    font-size: 0.7rem;
    padding: 2px 8px;
  }

  .filters-grid {
    padding: 10px 12px;
    gap: 10px;
  }

  .category-btn-compact {
    font-size: 0.75rem;
    padding: 3px 6px;
  }

  .price-input-compact {
    max-width: 60px;
    font-size: 0.8rem;
    padding: 4px 6px;
  }

  .preset-btn-compact {
    font-size: 0.7rem;
    padding: 3px 6px;
  }

  .toggle-slider-compact {
    width: 32px;
    height: 18px;
  }

  .toggle-slider-compact::before {
    width: 14px;
    height: 14px;
  }

  .toggle-input-compact:checked + .toggle-slider-compact::before {
    transform: translateX(14px);
  }

  .toggle-text-compact {
    font-size: 0.85rem;
  }

  .service-name {
    font-size: 1.1rem;
  }

  .service-description {
    font-size: 0.85rem;
  }

  .price-amount {
    font-size: 1.5rem;
  }

  .btn {
    padding: 12px 14px;
    font-size: 0.9rem;
  }

  .service-content {
    padding: 12px;
  }

  .provider-info {
    padding: 8px;
  }
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  grid-column: 1 / -1;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Focus styles for accessibility */
.search-input:focus,
.category-btn:focus,
.btn:focus,
.favorite-btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .service-card {
    border: 2px solid #000;
  }

  .btn-primary {
    background: #000;
    border-color: #000;
  }

  .btn-outline {
    border-color: #000;
    color: #000;
  }
}
</style>