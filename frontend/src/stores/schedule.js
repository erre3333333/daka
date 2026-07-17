import { defineStore } from 'pinia'
import { ref } from 'vue'
import { scheduleApi } from '../api'

export const useScheduleStore = defineStore('schedule', () => {
  const schedules = ref([])
  const loading = ref(false)

  const fetchSchedules = async () => {
    loading.value = true
    try {
      schedules.value = await scheduleApi.getAll()
    } finally {
      loading.value = false
    }
  }

  const addSchedule = async (schedule) => {
    await scheduleApi.create(schedule)
    await fetchSchedules()
  }

  const updateSchedule = async (id, data) => {
    await scheduleApi.update(id, data)
    await fetchSchedules()
  }

  const deleteSchedule = async (id) => {
    await scheduleApi.delete(id)
    await fetchSchedules()
  }

  return {
    schedules,
    loading,
    fetchSchedules,
    addSchedule,
    updateSchedule,
    deleteSchedule
  }
})
