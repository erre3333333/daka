<template>
  <div class="checkin-view">
    <div class="header">
      <div class="greeting">{{ greeting }}</div>
      <div class="clock">{{ clock }}</div>
      <div class="date">{{ dateStr }}</div>
    </div>
    
    <div class="container">
      <div class="encourage" v-if="encourage">{{ encourage }}</div>
      
      <van-cell-group inset>
        <van-cell
          v-for="schedule in schedules"
          :key="schedule.id"
          :title="schedule.label"
          :value="getTime(schedule)"
          :label="getStatusLabel(schedule.id)"
        >
          <template #right-icon>
            <van-button
              v-if="getStatus(schedule.id) === 'missed'"
              type="primary"
              size="small"
              @click="doCheckin(schedule.id)"
            >
              打卡
            </van-button>
            <van-button
              v-else
              type="default"
              size="small"
              @click="cancelCheckin(schedule.id)"
            >
              重置
            </van-button>
          </template>
        </van-cell>
      </van-cell-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { useCheckinStore } from '../stores/checkin'

const scheduleStore = useScheduleStore()
const checkinStore = useCheckinStore()

const now = ref(new Date())
const encourage = ref('')

const encourages = [
  '今天也是元气满满的一天！',
  '每一步都是进步，加油！',
  '坚持就是胜利，你最棒！',
  '相信自己，你可以的！',
  '每一天都是新的开始！',
  '保持微笑，好运自来！',
  '你比想象中更强大！',
  '努力的你，值得被看见！',
  '小小的努力，大大的改变！',
  '今天也要开开心心的！'
]

const greeting = computed(() => {
  const hour = now.value.getHours()
  if (hour < 6) return '夜深了，注意休息哦~'
  if (hour < 12) return '早上好，新的一天开始啦~'
  if (hour < 14) return '中午好，记得吃饭哦~'
  if (hour < 18) return '下午好，继续加油~'
  if (hour < 22) return '晚上好，今天辛苦了~'
  return '夜深了，早点休息哦~'
})

const clock = computed(() => {
  const h = now.value.getHours().toString().padStart(2, '0')
  const m = now.value.getMinutes().toString().padStart(2, '0')
  return `${h}:${m}`
})

const dateStr = computed(() => {
  const d = now.value
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `${d.getMonth() + 1}月${d.getDate()}日 周${weekdays[d.getDay()]}`
})

const schedules = computed(() => scheduleStore.schedules)

const getTime = (schedule) => {
  return `${schedule.hour.toString().padStart(2, '0')}:${schedule.minute.toString().padStart(2, '0')}`
}

const getStatus = (slotId) => {
  return checkinStore.getCheckinStatus(slotId)
}

const getStatusLabel = (slotId) => {
  const status = getStatus(slotId)
  if (status === 'done') return '✅ 已完成'
  if (status === 'skipped') return '⏭️ 已跳过'
  return '⏳ 待打卡'
}

const doCheckin = async (slotId) => {
  const date = now.value.toISOString().slice(0, 10)
  await checkinStore.doCheckin({ date, slot_id: slotId, status: 'done' })
  encourage.value = encourages[Math.floor(Math.random() * encourages.length)]
}

const cancelCheckin = async (slotId) => {
  const date = now.value.toISOString().slice(0, 10)
  await checkinStore.cancelCheckin(date, slotId)
}

let timer = null

onMounted(async () => {
  await scheduleStore.fetchSchedules()
  const date = now.value.toISOString().slice(0, 10)
  await checkinStore.fetchCheckins(date)
  
  timer = setInterval(() => {
    now.value = new Date()
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.checkin-view {
  min-height: 100vh;
  background: var(--bg);
}

.header {
  background: linear-gradient(135deg, #FFB5C2 0%, #FF8FAB 30%, #D4A5FF 70%, #A8E6CF 100%);
  color: #fff;
  padding: 28px 20px 36px;
  text-align: center;
  border-radius: 0 0 36px 36px;
}

.greeting {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.clock {
  font-size: 56px;
  font-weight: 400;
  letter-spacing: 6px;
}

.date {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 8px;
}

.container {
  max-width: 480px;
  margin: 0 auto;
  padding: 16px;
}

.encourage {
  background: rgba(255, 255, 255, 0.88);
  border-radius: 20px;
  padding: 16px;
  margin-bottom: 16px;
  text-align: center;
  font-size: 16px;
  color: var(--pink-dark);
  box-shadow: var(--shadow);
}
</style>
