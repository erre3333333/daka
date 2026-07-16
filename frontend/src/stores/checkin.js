import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
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

  const getMood = (slotId) => {
    const checkin = checkins.value.find(c => c.slot_id === slotId)
    return checkin?.mood || 3
  }

  const setMood = async (date, slotId, mood) => {
    const checkin = checkins.value.find(c => c.slot_id === slotId)
    if (checkin) {
      await checkinApi.create({
        date,
        slot_id: slotId,
        status: checkin.status,
        mood
      })
      await fetchCheckins(date)
    }
  }

  const completionRate = computed(() => {
    const done = checkins.value.filter(c => c.status === 'done').length
    return checkins.value.length > 0 ? Math.round(done / checkins.value.length * 100) : 0
  })

  return {
    checkins,
    loading,
    fetchCheckins,
    doCheckin,
    cancelCheckin,
    getCheckinStatus,
    getMood,
    setMood,
    completionRate
  }
})
