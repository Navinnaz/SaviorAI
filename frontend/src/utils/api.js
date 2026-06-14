const API_BASE = '/api/dashboard'
const API_KEY = 'SaviorAI_dev_key_2024'

// Get institution ID from localStorage or use default
const getInstitutionId = () => {
  return localStorage.getItem('institutionId') || '06d5af82-b343-4ccc-a5e9-6f01bebfaf41'
}

export const setInstitutionId = (id) => {
  localStorage.setItem('institutionId', id)
}

const fetchAPI = async (endpoint) => {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    }
  })
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  return response.json()
}

export const getOverview = () => {
  const instId = getInstitutionId()
  return fetchAPI(`/${instId}/overview`)
}

export const getHeatmap = () => {
  const instId = getInstitutionId()
  return fetchAPI(`/${instId}/heatmap`)
}

export const getStudentProfile = (studentId) => {
  return fetchAPI(`/student/${studentId}/profile`)
}

export const getCohorts = () => {
  const instId = getInstitutionId()
  return fetchAPI(`/${instId}/cohorts`)
}

export const getRecentInterventions = (limit = 20) => {
  const instId = getInstitutionId()
  return fetchAPI(`/interventions/recent?institution_id=${instId}&limit=${limit}`)
}

