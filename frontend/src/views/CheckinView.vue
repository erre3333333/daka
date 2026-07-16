<template>
  <div class="checkin-view">
    <!-- 浮动装饰 -->
    <div class="floating-deco">
      <div class="deco heart">❤️</div>
      <div class="deco">🌸</div>
      <div class="deco heart">💗</div>
      <div class="deco">✨</div>
      <div class="deco heart">💖</div>
      <div class="deco">🌷</div>
      <div class="deco heart">💕</div>
      <div class="deco">🌟</div>
      <div class="deco heart">💝</div>
      <div class="deco">🎀</div>
      <div class="deco heart">❣️</div>
      <div class="deco">🦋</div>
      <div class="deco heart">🩷</div>
      <div class="deco">🌺</div>
      <div class="deco heart">♥️</div>
      <div class="deco">💫</div>
      <div class="deco heart">💓</div>
      <div class="deco">🍭</div>
    </div>

    <div class="card" v-if="schedules.length === 0">
      <div class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 64 64" fill="none" stroke="var(--pink)" stroke-width="2">
            <rect x="12" y="8" width="40" height="48" rx="6"/>
            <path d="M22 20h20M22 30h20M22 40h12"/>
            <circle cx="48" cy="48" r="12" fill="var(--mint-light)" stroke="var(--mint)"/>
            <path d="M44 48l3 3 5-6" stroke="var(--mint)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <p>还没有作息计划呢<br>去设置页面添加吧 💕</p>
      </div>
    </div>

    <div class="card" v-else>
      <div
        class="slot"
        v-for="schedule in schedules"
        :key="schedule.id"
        :class="{ done: getStatus(schedule.id) === 'done', skipped: getStatus(schedule.id) === 'skip' }"
      >
        <div class="slot-icon">{{ getIcon(schedule.id) }}</div>
        <div class="info">
          <div class="label">
            {{ schedule.label }}
            <small class="schedule-time">{{ getTime(schedule) }}</small>
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
            <span class="status-badge done">✓</span>
          </template>
          <template v-else-if="getStatus(schedule.id) === 'skip'">
            <span class="status-badge skip">→</span>
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
  position: relative;
  overflow: visible;
}

.floating-deco {
  position: fixed; inset: 0; pointer-events: none; z-index: 10; overflow: hidden;
}
.floating-deco .deco {
  position: absolute; animation: floatDeco 12s infinite linear; opacity: 0.4;
}
.floating-deco .deco.heart {
  color: #FF4D6A; text-shadow: 0 0 8px rgba(255,77,106,0.4);
}
@keyframes floatDeco {
  0% { transform: translateY(100vh) rotate(0deg) scale(0.5); opacity: 0; }
  10% { opacity: 0.35; }
  90% { opacity: 0.3; }
  100% { transform: translateY(-15vh) rotate(540deg) scale(1); opacity: 0; }
}
.floating-deco .deco:nth-child(1) { left: 3%; animation-duration: 11s; animation-delay: 0s; font-size: 28px; }
.floating-deco .deco:nth-child(2) { left: 10%; animation-duration: 13s; animation-delay: 1s; font-size: 20px; }
.floating-deco .deco:nth-child(3) { left: 18%; animation-duration: 10s; animation-delay: 3s; font-size: 32px; }
.floating-deco .deco:nth-child(4) { left: 26%; animation-duration: 14s; animation-delay: 0s; font-size: 18px; }
.floating-deco .deco:nth-child(5) { left: 34%; animation-duration: 12s; animation-delay: 2s; font-size: 30px; }
.floating-deco .deco:nth-child(6) { left: 42%; animation-duration: 15s; animation-delay: 4s; font-size: 22px; }
.floating-deco .deco:nth-child(7) { left: 50%; animation-duration: 11s; animation-delay: 1s; font-size: 34px; }
.floating-deco .deco:nth-child(8) { left: 58%; animation-duration: 13s; animation-delay: 3s; font-size: 18px; }
.floating-deco .deco:nth-child(9) { left: 65%; animation-duration: 10s; animation-delay: 0s; font-size: 28px; }
.floating-deco .deco:nth-child(10) { left: 72%; animation-duration: 14s; animation-delay: 2s; font-size: 22px; }
.floating-deco .deco:nth-child(11) { left: 79%; animation-duration: 12s; animation-delay: 4s; font-size: 30px; }
.floating-deco .deco:nth-child(12) { left: 86%; animation-duration: 11s; animation-delay: 1s; font-size: 18px; }
.floating-deco .deco:nth-child(13) { left: 92%; animation-duration: 13s; animation-delay: 3s; font-size: 26px; }
.floating-deco .deco:nth-child(14) { left: 7%; animation-duration: 15s; animation-delay: 5s; font-size: 20px; }
.floating-deco .deco:nth-child(15) { left: 46%; animation-duration: 10s; animation-delay: 2s; font-size: 28px; }
.floating-deco .deco:nth-child(16) { left: 55%; animation-duration: 14s; animation-delay: 0s; font-size: 18px; }
.floating-deco .deco:nth-child(17) { left: 30%; animation-duration: 12s; animation-delay: 4s; font-size: 32px; }
.floating-deco .deco:nth-child(18) { left: 68%; animation-duration: 11s; animation-delay: 1s; font-size: 22px; }

.card {
  background: var(--card);
  backdrop-filter: blur(16px);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 14px;
  overflow: hidden;
  border: 1px solid rgba(248,164,184,0.12);
}

.empty-state {
  text-align: center;
  padding: 52px 20px;
  color: var(--text-light);
}
.empty-icon {
  width: 72px; height: 72px; margin: 0 auto 16px;
  background: var(--pink-light); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.empty-icon svg { width: 36px; height: 36px; }
.empty-state p { font-size: 14px; line-height: 1.9; }

.slot {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border-bottom: 1px solid rgba(248,164,184,0.08);
  transition: background 0.2s; position: relative;
}
.slot:last-child { border-bottom: none; }
.slot:active { background: rgba(248,164,184,0.04); }

.slot-icon {
  width: 48px; height: 48px; border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
  background: linear-gradient(135deg, var(--pink-light), var(--peach-light));
  transition: all 0.3s;
}
.slot.done .slot-icon {
  background: linear-gradient(135deg, var(--mint-light), var(--lavender-light));
}
.slot.skipped .slot-icon {
  background: var(--cream);
  opacity: 0.7;
}

.info { flex: 1; min-width: 0; }
.label { font-size: 16px; font-weight: 400; color: var(--text); }
.schedule-time {
  font-size: 12px; color: var(--text-light); margin-left: 6px;
  background: rgba(248,164,184,0.08); padding: 2px 8px; border-radius: 8px;
}
.meta { font-size: 12px; color: var(--text-light); margin-top: 4px; letter-spacing: 0.5px; }
.mood-line { display: flex; gap: 4px; margin-top: 6px; }
.mood-dot {
  width: 32px; height: 32px; border-radius: 50%; border: 2px solid transparent;
  cursor: pointer; font-size: 13px; display: flex; align-items: center;
  justify-content: center; transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: var(--pink-light);
}
.mood-dot:active { transform: scale(0.8); }
.mood-dot.active {
  border-color: var(--pink); background: var(--pink-light);
  transform: scale(1.15); box-shadow: 0 2px 10px rgba(248,164,184,0.3);
}

.actions { display: flex; gap: 6px; flex-shrink: 0; align-items: center; }
.btn {
  padding: 8px 16px; border-radius: 20px; border: none;
  font-family: inherit; font-size: 13px; cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); white-space: nowrap;
}
.btn:active { transform: scale(0.88); }
.btn-done {
  background: linear-gradient(135deg, var(--pink), var(--pink-light)); color: #fff;
  box-shadow: 0 3px 12px rgba(248,164,184,0.3);
}
.btn-skip { background: var(--cream); color: var(--text-light); }

.status-badge {
  width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 600;
}
.status-badge.done {
  background: var(--mint-light); color: #6BBF8A;
}
.status-badge.skip {
  background: var(--cream); color: var(--text-light);
}
</style>
