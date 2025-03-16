<template>
  <div class="clients-list">
    <div class="all-clients-option">
      <div 
        class="client-card"
        :class="{ 'selected': selectedClientId === null }"
        @click="selectClient(null)"
      >
        <h3>All Clients</h3>
      </div>
    </div>
        
    <div v-if="loading" class="loading">
      Loading clients...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else>
      <div v-if="clients.length === 0" class="empty-state">
        No clients found.
      </div>
      
      <div v-else class="clients-grid">
        <div 
          v-for="client in clients" 
          :key="client.id" 
          class="client-card"
          :class="{ 'selected': selectedClientId === client.id }"
          @click="selectClient(client.id)"
        >
          <h3>{{ client.name }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSupabaseStore } from '@/stores/supabase'

const store = useSupabaseStore()

// Computed properties
const clients = computed(() => store.clients)
const loading = computed(() => store.loading.clients)
const error = computed(() => store.error)
const selectedClientId = computed(() => store.filters.clientId)

// Methods
function selectClient(clientId) {
  if (selectedClientId.value === clientId) {
    // If clicking the already selected client, deselect it
    store.setFilter('clientId', null)
  } else {
    store.setFilter('clientId', clientId)
  }
}
</script>

<style scoped>
.clients-list {
  margin-bottom: 2rem;
}

.all-clients-option {
  margin-bottom: 1rem;
}

.clients-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.client-card {
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #2c3e50;
  color: #f5f5f5;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60px;
}

.client-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  background-color: #34495e;
}

.client-card.selected {
  border-color: #42b883;
  background-color: rgba(66, 184, 131, 0.2);
  color: #fff;
  font-weight: 500;
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