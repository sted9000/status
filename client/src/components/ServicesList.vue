<template>
  <div class="services-list">
    
    <div class="filter-controls">
      <div class="filter-group">
        
        <select id="status-filter" v-model="statusFilter" @change="applyStatusFilter">
          <option value="">All Statuses</option>
          <option value="passed">Passed</option>
          <option value="failed">Failed</option>
        </select>
      </div>
      
      <div class="filter-group">
        
        <select id="platform-filter" v-model="platformFilter" @change="applyPlatformFilter">
          <option value="">All Platforms</option>
          <option v-for="platform in availablePlatforms" :key="platform" :value="platform">
            {{ platform }}
          </option>
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      Loading services...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else>
      <div v-if="filteredServices.length === 0" class="empty-state">
        <p v-if="selectedClientId">No services found for the selected client.</p>
        <p v-else-if="statusFilter">No services match the current status filter.</p>
        <p v-else>No services found.</p>
      </div>
      
      <div v-else-if="filteredServicesWithStatus.length === 0" class="empty-state">
        <p v-if="statusFilter && platformFilter">No services match the current status and platform filters.</p>
        <p v-else-if="statusFilter">No services match the current status filter.</p>
        <p v-else-if="platformFilter">No services match the current platform filter.</p>
        <p v-else>No services found with the current filters.</p>
      </div>
      
      <div v-else class="services-grid">
        <div 
          v-for="service in filteredServicesWithStatus" 
          :key="service.id" 
          class="service-card"
          :class="[
            service.status ? getStatusClass(service.status) : ''
          ]"
        >
          <h3>{{ service.name }}</h3>
          <div class="platform-badge">{{ service.platform }}</div>
          
          <div v-if="service.status" class="status-section">
            <div class="status-badge" :class="getStatusClass(service.status)">
              {{ service.status }}
            </div>
            <p class="status-message">{{ service.message }}</p>
            <p class="status-meta">
              <span>Last updated: {{ formatDate(service.updatedAt) }}</span>
              <span v-if="service.toolName">Tool: {{ service.toolName }}</span>
            </p>
          </div>
          <div v-else class="status-section no-status">
            <p>No status updates available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSupabaseStore } from '@/stores/supabase'

const store = useSupabaseStore()

// Local state for filters
const statusFilter = ref('')
const platformFilter = ref('')

// Computed properties
const filteredServices = computed(() => store.filteredServices)
const serviceStatuses = computed(() => store.serviceStatuses)
const loading = computed(() => store.loading.services || store.loading.serviceUpdates)
const error = computed(() => store.error)
const selectedClientId = computed(() => store.filters.clientId)

// Get unique platforms for the filter dropdown
const availablePlatforms = computed(() => {
  const platforms = new Set(filteredServices.value.map(service => service.platform))
  return Array.from(platforms).sort()
})

// Combine services with their latest status
const filteredServicesWithStatus = computed(() => {
  // Create a map of service statuses by service ID for quick lookup
  const statusMap = new Map(
    serviceStatuses.value.map(status => [status.serviceId, status])
  )
  
  return filteredServices.value
    .map(service => {
      const status = statusMap.get(service.id)
      if (status) {
        return {
          ...service,
          status: status.status,
          message: status.message,
          updatedAt: status.updatedAt,
          toolName: status.toolName
        }
      }
      return service
    })
    .filter(service => {
      // Apply status filter if set
      if (statusFilter.value && service.status) {
        if (service.status !== statusFilter.value) {
          return false
        }
      }
      
      // Apply platform filter if set
      if (platformFilter.value && service.platform) {
        if (service.platform !== platformFilter.value) {
          return false
        }
      }
      
      return true
    })
})

// Methods
function applyStatusFilter() {
  // We handle filtering locally in the computed property
  // This is just to trigger reactivity
  statusFilter.value = statusFilter.value
}

function applyPlatformFilter() {
  // We handle filtering locally in the computed property
  // This is just to trigger reactivity
  platformFilter.value = platformFilter.value
}

function getStatusClass(status) {
  if (!status) return ''
  
  switch (status.toLowerCase()) {
    case 'passed':
      return 'status-passed'
    case 'failed':
      return 'status-failed'
    default:
      return ''
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString(undefined, {
    year: 'numeric',
    month: 'numeric', 
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  })
}
</script>

<style scoped>
.services-list {
  margin-bottom: 2rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  color: #f5f5f5;
  font-weight: 500;
}

select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #2c3e50;
  color: #f5f5f5;
  font-size: 0.9rem;
}

select:focus {
  outline: none;
  border-color: #42b883;
  box-shadow: 0 0 0 2px rgba(66, 184, 131, 0.2);
}

select option {
  background-color: #2c3e50;
  color: #f5f5f5;
}

.services-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  width: 100%;
}

.service-card {
  border: 1px solid #444;
  border-radius: 4px;
  padding: 1rem;
  position: relative;
  color: #f5f5f5;
  background-color: #2c3e50;
  display: flex;
  flex-direction: column;
  min-height: 150px; /* Ensure minimum height */
  width: 280px; /* Fixed width for each card */
  margin-bottom: 0.5rem;
}

.service-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  background-color: #34495e;
}

/* Status-specific styling */
.service-card.status-passed {
  border-color: #27ae60;
  background-color: rgba(46, 204, 113, 0.15);
}

.service-card.status-failed {
  border-color: #c0392b;
  background-color: rgba(231, 76, 60, 0.15);
}

.platform-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #2a3f54;
  color: #42b883;
  border: 1px solid #42b883;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-section {
  margin: 1rem 0;
  padding: 0.75rem;
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.2);
  color: #f5f5f5;
}

.no-status {
  color: #bbb;
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.status-passed {
  background-color: rgba(46, 204, 113, 0.3);
  color: #2ecc71;
}

.status-failed {
  background-color: rgba(231, 76, 60, 0.3);
  color: #e74c3c;
}

.status-message {
  margin: 0.5rem 0;
  font-size: 0.95rem;
  color: #f5f5f5;
}

.status-meta {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  font-size: 0.8rem;
  color: #bbb;
  margin-top: 0.5rem;
}

.loading, .error, .empty-state {
  padding: 1rem;
  text-align: center;
  color: #bbb;
}

.error {
  color: #e74c3c;
}
</style> 