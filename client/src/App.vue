<script setup>
import { onMounted } from 'vue'
import { useSupabaseStore } from '@/stores/supabase'
import ClientsList from './components/ClientsList.vue'
import ServicesList from './components/ServicesList.vue'

const store = useSupabaseStore()

onMounted(() => {
  // Fetch initial data
  store.fetchClients()
  store.fetchServices()
  store.fetchUpdates()
  store.fetchPlatforms()
  // Setup realtime subscriptions
  store.setupRealtimeSubscriptions()
})
</script>

<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <h2>Clients</h2>
      <ClientsList />
    </aside>
    
    <main class="main-content">
      <h2>Services</h2>
      <ServicesList />
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  width: 100vw; /* Full viewport width */
  overflow: hidden; /* Prevent double scrollbars */
}

.sidebar {
  width: 300px; /* Increased from 250px */
  background-color: #1a2634;
  border-right: 1px solid #444;
  padding: 1rem;
  overflow-y: auto;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  height: 100%;
  flex-shrink: 0;
}

.sidebar h2, .main-content h2 {
  color: #42b883;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #444;
  position: sticky;
  top: 0;
  background-color: inherit;
  z-index: 1;
}

.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
  overflow-y: auto;
  height: 100%;
  min-width: 0;
}

@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    max-height: 40vh;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .main-content {
    height: auto;
    min-height: 60vh;
  }
}
</style>
