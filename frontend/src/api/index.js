import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const scheduleApi = {
  getAll: () => api.get('/schedules'),
  create: (data) => api.post('/schedules', data),
  update: (id, data) => api.put(`/schedules/${id}`, data),
  delete: (id) => api.delete(`/schedules/${id}`)
}

export const checkinApi = {
  getByDate: (date) => api.get('/checkins', { params: { date } }),
  create: (data) => api.post('/checkins', data),
  delete: (data) => api.delete('/checkins', { data })
}

export const statsApi = {
  get: (range) => api.get('/stats', { params: { range } })
}

export const weatherApi = {
  get: (city) => api.get('/weather', { params: { city } })
}

export const aiApi = {
  analyze: (range) => api.post('/ai/analyze', null, { params: { range } }),
  voice: (text) => api.post('/ai/voice', null, { params: { text } })
}

export default api
