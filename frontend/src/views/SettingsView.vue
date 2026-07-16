<template>
  <div class="settings-view">
    <div class="card settings-wrap">
      <div class="title">⚙️ 我的作息</div>
      <div class="settings-hint">
        <span>✏️ 点名字可改名</span>
        <span>🕐 点时间可修改</span>
        <span>✅ 勾选启用</span>
        <span>✕ 删除项目</span>
      </div>
      
      <div class="set-field" v-for="schedule in schedules" :key="schedule.id">
        <input
          type="text"
          :value="schedule.label"
          class="set-label"
          maxlength="10"
          @change="(e) => updateLabel(schedule.id, e.target.value)"
        >
        <input
          type="time"
          :value="getTime(schedule)"
          class="set-time"
          @change="(e) => updateTime(schedule.id, e.target.value)"
        >
        <input
          type="checkbox"
          :checked="schedule.enabled"
          class="set-enabled"
          @change="(e) => toggleEnabled(schedule, e.target.checked)"
        >
        <button class="set-del" @click="deleteSchedule(schedule.id)">✕</button>
      </div>

      <button class="add-btn" @click="addSchedule">＋ 新增项目</button>
      <button class="save-btn" @click="saveAll">💾 保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useScheduleStore } from '../stores/schedule'

const scheduleStore = useScheduleStore()
const updateTip = inject('updateTip')

const schedules = ref([])

const getTime = (schedule) => {
  return `${schedule.hour.toString().padStart(2, '0')}:${schedule.minute.toString().padStart(2, '0')}`
}

const updateLabel = async (id, label) => {
  await scheduleStore.updateSchedule(id, { label })
}

const updateTime = async (id, time) => {
  const [h, m] = time.split(':').map(Number)
  await scheduleStore.updateSchedule(id, { hour: h, minute: m })
}

const toggleEnabled = async (schedule, enabled) => {
  await scheduleStore.updateSchedule(schedule.id, { enabled })
}

const deleteSchedule = async (id) => {
  if (!confirm('确定删除这个项目吗？')) return
  await scheduleStore.deleteSchedule(id)
  await loadSchedules()
  updateTip('🗑️', '项目已删除')
}

const addSchedule = async () => {
  const name = prompt('项目名称：')
  if (!name?.trim()) return
  const id = 'custom_' + Date.now()
  await scheduleStore.addSchedule({
    id,
    label: name.trim(),
    hour: 8,
    minute: 0,
    enabled: true
  })
  await loadSchedules()
  updateTip('✅', `已添加「${name.trim()}」`)
}

const saveAll = async () => {
  updateTip('💾', '保存成功！')
}

const loadSchedules = async () => {
  await scheduleStore.fetchSchedules()
  schedules.value = scheduleStore.schedules
}

onMounted(loadSchedules)
</script>

<style scoped>
.settings-view {
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
}

.settings-wrap { padding: 20px; }
.settings-wrap .title { font-size: 16px; font-weight: 400; margin-bottom: 8px; letter-spacing: 1px; }

.settings-hint {
  display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px;
  padding: 10px 14px; background: rgba(255,182,193,0.06); border-radius: 12px;
  border: 1px solid rgba(255,182,193,0.12);
}
.settings-hint span {
  font-size: 11px; color: var(--text-light); white-space: nowrap;
}

.set-field {
  display: flex; align-items: center; gap: 10px; margin-bottom: 12px;
  padding: 12px 14px; background: rgba(255,182,193,0.05); border-radius: 14px;
}
.set-field .set-label {
  width: 72px; padding: 6px 8px; border: 1.5px solid rgba(255,182,193,0.2); border-radius: 10px;
  font-family: inherit; font-size: 14px; background: #fff; color: var(--text); outline: none;
  flex-shrink: 0;
}
.set-field .set-label:focus { border-color: var(--pink); }

.set-del {
  width: 30px; height: 30px; border-radius: 50%; border: 1.5px solid #E8D5DE;
  background: none; color: var(--text-light); font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  transition: all 0.2s;
}
.set-del:active { background: #FFE0E6; border-color: var(--pink); color: var(--pink); }

.add-btn {
  width: 100%; padding: 12px; border: 2px dashed rgba(255,182,193,0.3); border-radius: 16px;
  background: none; font-family: inherit; font-size: 14px; color: var(--text-light);
  cursor: pointer; margin-top: 8px; transition: all 0.2s; letter-spacing: 1px;
}
.add-btn:active { background: rgba(255,182,193,0.06); border-color: var(--pink); }

.set-field input[type=time] {
  flex: 1; padding: 8px 12px; border: 1.5px solid rgba(255,182,193,0.2); border-radius: 10px;
  font-family: inherit; font-size: 14px; background: #fff; color: var(--text); outline: none;
}
.set-field input[type=time]:focus { border-color: var(--pink); }
.set-field input[type=checkbox] { width: 22px; height: 22px; accent-color: var(--pink); cursor: pointer; }

.save-btn {
  width: 100%; padding: 14px; border: none; border-radius: 16px; font-family: inherit;
  font-size: 16px; font-weight: 400; cursor: pointer; margin-top: 8px;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, #FFD3B6, #FFE4B5); color: var(--text);
  box-shadow: 0 3px 12px rgba(255,211,182,0.3); letter-spacing: 1px;
}
.save-btn:active { transform: scale(0.95); }
</style>
