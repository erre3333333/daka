import { defineStore } from 'pinia'
import { ref } from 'vue'
import { checkinApi } from '../api'

export const useCheckinStore = defineStore('checkin', () => {
  const checkins = ref([])
  const loading = ref(false)

  const fetchCheckins = async (date) => {
    loading.value = true
    try {
      checkins.value = await checkinApi.getByDate(date)
    } finally {
      loading.value = false
    }
  }

  const doCheckin = async (data) => {
    await checkinApi.create(data)
    await fetchCheckins(data.date)
  }

  const cancelCheckin = async (date, slotId) => {
    await checkinApi.delete({ date, slot_id: slotId })
    await fetchCheckins(date)
  }

  const getCheckinStatus = (slotId) => {
    const checkin = checkins.value.find(c => c.slot_id === slotId)
    return checkin?.status || 'missed'
  }

  return {
    checkins,
    loading,
    fetchCheckins,
    doCheckin,
    cancelCheckin,
    getCheckinStatus
  }
})
