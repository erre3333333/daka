<template>
  <div class="checkin-view">
    <div class="card" v-if="schedules.length === 0">
      <div class="empty-state">
        <div class="icon">📋</div>
        <p>还没有作息计划呢<br>去设置页面添加吧 💕</p>
      </div>
    </div>

    <div class="card" v-else>
      <div
        class="slot"
        v-for="schedule in schedules"
        :key="schedule.id"
        :class="{ done: getStatus(schedule.id) === 'done' }"
      >
        <div class="time-icon">{{ getIcon(schedule.id) }}</div>
        <div class="info">
          <div class="label">
            {{ schedule.label }}
            <small>{{ getTime(schedule) }}</small>
          </div>
          <div class="mood-line" v-if="getStatus(schedule.id) === 'done'">
            <span
              v-for="(mood, i) in moods"
              :key="i"
              class="mood-dot"
              :class="{ active: getMood(schedule.id) === i + 1 }"
              @click="setMood(schedule.id, i + 1)"
            >{{ mood }}</span>
          </div>
          <div class="meta" v-else>{{ getNote(schedule.id) }}</div>
        </div>
        <div class="actions">
          <template v-if="getStatus(schedule.id) === 'done'">
            <span class="status-badge done">✅</span>
          </template>
          <template v-else-if="getStatus(schedule.id) === 'skip'">
            <span class="status-badge skip">⏭️</span>
          </template>
          <template v-else>
            <button class="btn btn-done" @click="doCheckin(schedule.id, 'done')">完成</button>
            <button class="btn btn-skip" @click="doCheckin(schedule.id, 'skip')">跳过</button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { useCheckinStore } from '../stores/checkin'

const scheduleStore = useScheduleStore()
const checkinStore = useCheckinStore()
const updateTip = inject('updateTip')

const moods = ['😞', '😐', '😊', '😄', '🥰']

const scheduleIcons = {
  wake: '☀️', breakfast: '🥐', lunch: '🍚', nap: '😴',
  dinner: '🍜', exercise: '🏃‍♀️', sleep: '🌙'
}

const scheduleNotes = {
  wake: '新的一天开始啦',
  breakfast: '早餐要吃好哦',
  lunch: '中午记得吃饱饱',
  nap: '休息一下充充电',
  dinner: '晚餐也要吃好',
  exercise: '动起来～',
  sleep: '早睡早起身体好'
}

const schedules = computed(() => scheduleStore.schedules)

const getIcon = (id) => scheduleIcons[id] || '⏰'
const getTime = (s) => `${s.hour.toString().padStart(2, '0')}:${s.minute.toString().padStart(2, '0')}`
const getStatus = (slotId) => checkinStore.getCheckinStatus(slotId)
const getMood = (slotId) => checkinStore.getMood(slotId)
const getNote = (id) => scheduleNotes[id] || ''

const doCheckin = async (slotId, status) => {
  const date = new Date().toISOString().slice(0, 10)
  await checkinStore.doCheckin({ date, slot_id: slotId, status })
  updateTip('💖', '打卡成功！宝宝真棒 ✨')
  setTimeout(() => {
    const tips = [
      { icon: '💪', text: '今天也要元气满满哦！' },
      { icon: '💖', text: '和你在一起的每一天都是礼物' },
      { icon: '✨', text: '你的存在就是我的小确幸' },
    ]
    const t = tips[Math.floor(Math.random() * tips.length)]
    updateTip(t.icon, t.text)
  }, 2500)
}

const setMood = async (slotId, mood) => {
  const date = new Date().toISOString().slice(0, 10)
  await checkinStore.setMood(date, slotId, mood)
  const msgs = ['抱抱你 🫂', '放轻松 🍃', '还不错 😊', '真好呀 🥰', '太开心了 🎉']
  updateTip('💖', msgs[mood - 1] || msgs[2])
  setTimeout(() => {
    const tips = [
      { icon: '💪', text: '今天也要元气满满哦！' },
      { icon: '💖', text: '和你在一起的每一天都是礼物' },
    ]
    const t = tips[Math.floor(Math.random() * tips.length)]
    updateTip(t.icon, t.text)
  }, 2500)
}
</script>

<style scoped>
.checkin-view {
  min-height: 100vh;
  background: var(--bg);
}

.card {
  background: var(--card);
  backdrop-filter: blur(12px);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 16px;
  overflow: hidden;
  border: 1.5px solid rgba(255,182,193,0.15);
  max-height: 60vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-light);
}
.empty-state .icon { font-size: 56px; margin-bottom: 12px; display: block; }
.empty-state p { font-size: 14px; line-height: 1.8; }

.slot {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 16px; border-bottom: 1px solid rgba(255,182,193,0.1);
  transition: all 0.3s; position: relative;
}
.slot:last-child { border-bottom: none; }
.slot .time-icon {
  width: 54px; height: 54px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
  background: linear-gradient(135deg, var(--pink-light), var(--peach));
  transition: all 0.3s; box-shadow: 0 3px 10px rgba(255,143,171,0.2);
}
.slot.done .time-icon {
  background: linear-gradient(135deg, var(--mint), #C8E6C9);
  box-shadow: 0 3px 10px rgba(168,230,207,0.3);
}
.slot .info { flex: 1; min-width: 0; }
.slot .label { font-size: 17px; font-weight: 400; color: var(--text); }
.slot .label small { font-weight: 400; color: var(--text-light); font-size: 13px; margin-left: 6px; }
.slot .meta { font-size: 12px; color: var(--text-light); margin-top: 3px; letter-spacing: 0.5px; }
.slot .mood-line { display: flex; gap: 5px; margin-top: 7px; }
.slot .mood-dot {
  width: 34px; height: 34px; border-radius: 50%; border: 2px solid transparent;
  cursor: pointer; font-size: 14px; display: flex; align-items: center;
  justify-content: center; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: #FFF0F2;
}
.slot .mood-dot:active { transform: scale(0.8); }
.slot .mood-dot.active { border-color: #FF8FAB; background: #FFE0E6; transform: scale(1.2); }
.slot .actions { display: flex; gap: 6px; flex-shrink: 0; align-items: center; }
.slot .btn {
  padding: 9px 18px; border-radius: 30px; border: none;
  font-family: inherit; font-size: 13px; font-weight: 400; cursor: pointer;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); white-space: nowrap;
}
.slot .btn:active { transform: scale(0.85); }
.btn-done {
  background: linear-gradient(135deg, #FF8FAB, #FFB5C2); color: #fff;
  box-shadow: 0 3px 12px rgba(255,143,171,0.35);
}
.btn-skip { background: #FFF0F2; color: var(--text-light); }
.slot .status-badge { font-size: 16px; }
</style>
