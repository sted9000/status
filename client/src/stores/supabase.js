import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { supabase } from '@/supabase'

export const useSupabaseStore = defineStore('supabase', () => {
  // State
  const clients = ref([])
  const services = ref([])
  const serviceUpdates = ref([])
  const loading = ref({
    clients: false,
    services: false,
    serviceUpdates: false
  })
  const error = ref(null)
  const filters = ref({
    clientId: null,
    serviceId: null,
    status: null,
    toolName: null
  })

  // Getters
  const filteredServices = computed(() => {
    if (!filters.value.clientId) return services.value
    return services.value.filter(service => service.client_id === filters.value.clientId)
  })

  const filteredServiceUpdates = computed(() => {
    let result = serviceUpdates.value

    if (filters.value.serviceId) {
      result = result.filter(update => update.service_id === filters.value.serviceId)
    }
    
    if (filters.value.status) {
      result = result.filter(update => update.status === filters.value.status)
    }
    
    if (filters.value.toolName) {
      result = result.filter(update => update.tool_name === filters.value.toolName)
    }
    
    return result
  })

  // New computed property for service statuses
  const serviceStatuses = computed(() => {
    // Create a map to store the latest update for each service
    const latestUpdates = new Map()
    
    // Process all service updates to find the latest for each service
    serviceUpdates.value.forEach(update => {
      const serviceId = update.service_id
      
      if (!latestUpdates.has(serviceId) || 
          new Date(update.updated_at) > new Date(latestUpdates.get(serviceId).updatedAt)) {
        // Map legacy status values to new passed/failed values if needed
        let status = update.status
        if (status === 'success') status = 'passed'
        else if (['error', 'warning'].includes(status)) status = 'failed'
        
        latestUpdates.set(serviceId, {
          serviceId,
          status: status,
          message: update.message,
          updatedAt: update.updated_at,
          toolName: update.tool_name
        })
      }
    })
    
    // Convert the map to an array
    return Array.from(latestUpdates.values())
  })

  // Actions
  async function fetchClients() {
    loading.value.clients = true
    error.value = null
    
    try {
      const { data, error: err } = await supabase
        .from('clients')
        .select('*')
        .order('name')
      
      if (err) throw err
      
      clients.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching clients:', err)
    } finally {
      loading.value.clients = false
    }
  }

  async function fetchServices() {
    loading.value.services = true
    error.value = null
    
    try {
      const { data, error: err } = await supabase
        .from('services')
        .select('*')
        .order('name')
      
      if (err) throw err
      
      services.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching services:', err)
    } finally {
      loading.value.services = false
    }
  }

  async function fetchServiceUpdates() {
    loading.value.serviceUpdates = true
    error.value = null
    
    try {
      const { data, error: err } = await supabase
        .from('service_updates')
        .select('*')
        .order('updated_at', { ascending: false })
      
      if (err) throw err
      
      serviceUpdates.value = data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching service updates:', err)
    } finally {
      loading.value.serviceUpdates = false
    }
  }

  function setFilter(filterName, value) {
    filters.value[filterName] = value
  }

  // Setup realtime subscriptions
  function setupRealtimeSubscriptions() {
    // Subscribe to changes in the clients table
    supabase
      .channel('clients-changes')
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table: 'clients' 
      }, (payload) => {
        console.log('Clients change received:', payload)
        fetchClients()
      })
      .subscribe()

    // Subscribe to changes in the services table
    supabase
      .channel('services-changes')
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table: 'services' 
      }, (payload) => {
        console.log('Services change received:', payload)
        fetchServices()
      })
      .subscribe()

    // Subscribe to changes in the service_updates table
    supabase
      .channel('service-updates-changes')
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table: 'service_updates' 
      }, (payload) => {
        console.log('Service updates change received:', payload)
        fetchServiceUpdates()
      })
      .subscribe()
  }

  return { 
    clients, 
    services, 
    serviceUpdates, 
    loading, 
    error, 
    filters,
    filteredServices,
    filteredServiceUpdates,
    serviceStatuses,
    fetchClients, 
    fetchServices, 
    fetchServiceUpdates,
    setFilter,
    setupRealtimeSubscriptions
  }
}) 