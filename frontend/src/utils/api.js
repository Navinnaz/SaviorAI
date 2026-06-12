const API_BASE = '/api/dashboard'
const API_KEY = 'guardianai_dev_key_2024'

// Get institution ID from localStorage or use default
const getInstitutionId = () => {
  return localStorage.getItem('institutionId') || '747f60be-c964-448f-879c-04291df5941d'
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
