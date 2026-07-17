import { defineStore } from 'pinia'
import { ref } from 'vue'
import { scheduleApi } from '../api'

export const useScheduleStore = defineStore('schedule', () => {
  const schedules = ref([])

  const fetchSchedules = async () => {
    schedules.value = await scheduleApi.getAll()
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
    fetchSchedules,
    addSchedule,
    updateSchedule,
    deleteSchedule
  }
})
