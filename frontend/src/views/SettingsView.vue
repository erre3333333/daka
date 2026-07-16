<template>
  <div class="settings-view">
    <div class="card settings-wrap">
      <div class="card-header">
        <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="var(--lavender)" stroke-width="2">
          <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        <div>
          <div class="title">我的作息</div>
          <div class="subtitle">自定义你的每日计划</div>
        </div>
      </div>

      <div class="settings-hint">
        <span class="hint-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          点名字改名
        </span>
        <span class="hint-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          点时间修改
        </span>
        <span class="hint-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M20 6L9 17l-5-5"/></svg>
          勾选启用
        </span>
        <span class="hint-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M18 6L6 18M6 6l12 12"/></svg>
          删除
        </span>
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
        <label class="set-check">
          <input
            type="checkbox"
            :checked="schedule.enabled"
            @change="(e) => toggleEnabled(schedule, e.target.checked)"
          >
          <span class="checkmark"></span>
        </label>
        <button class="set-del" @click="deleteSchedule(schedule.id)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <button class="add-btn" @click="addSchedule">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        新增项目
      </button>
      <button class="save-btn" @click="saveAll">保存</button>
    </div>

    <div class="card backup-card">
      <div class="card-header">
        <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="var(--mint)" stroke-width="2">
          <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
        </svg>
        <div>
          <div class="title">数据备份</div>
          <div class="subtitle">备份数据库到 GitHub</div>
        </div>
      </div>
      <button class="backup-btn" @click="triggerBackup" :disabled="backupLoading">
        <span v-if="backupLoading">备份中...</span>
        <span v-else>📤 备份到 GitHub</span>
      </button>
      <div class="backup-msg" v-if="backupMsg">{{ backupMsg }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { backupApi } from '../api'

const scheduleStore = useScheduleStore()
const updateTip = inject('updateTip')

const schedules = ref([])

const getTime = (schedule) =>
  `${schedule.hour.toString().padStart(2, '0')}:${schedule.minute.toString().padStart(2, '0')}`

const updateLabel = async (id, label) => await scheduleStore.updateSchedule(id, { label })
const updateTime = async (id, time) => {
  const [h, m] = time.split(':').map(Number)
  await scheduleStore.updateSchedule(id, { hour: h, minute: m })
}
const toggleEnabled = async (schedule, enabled) => await scheduleStore.updateSchedule(schedule.id, { enabled })

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
  await scheduleStore.addSchedule({ id, label: name.trim(), hour: 8, minute: 0, enabled: true })
  await loadSchedules()
  updateTip('✅', `已添加「${name.trim()}」`)
}

const saveAll = () => updateTip('💾', '保存成功！')

const backupLoading = ref(false)
const backupMsg = ref('')

const triggerBackup = async () => {
  backupLoading.value = true
  backupMsg.value = ''
  try {
    const res = await backupApi.trigger()
    backupMsg.value = `✅ 备份成功！commit: ${res.commit}`
    updateTip('📤', '数据库已备份到 GitHub')
  } catch (e) {
    const msg = e?.response?.data?.error || e.message
    backupMsg.value = `❌ 备份失败：${msg}`
  }
  backupLoading.value = false
}

const loadSchedules = async () => {
  await scheduleStore.fetchSchedules()
  schedules.value = scheduleStore.schedules
}

onMounted(loadSchedules)
</script>

<style scoped>
.settings-view { position: relative; }

.card {
  background: var(--card);
  backdrop-filter: blur(16px);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 14px;
  overflow: hidden;
  border: 1px solid rgba(248,164,184,0.12);
}

.card-header {
  display: flex; align-items: center; gap: 12px; padding: 20px 20px 12px;
}
.card-icon { width: 28px; height: 28px; flex-shrink: 0; }
.title { font-size: 16px; font-weight: 400; letter-spacing: 0.5px; }
.subtitle { font-size: 12px; color: var(--text-light); margin-top: 2px; }

.settings-hint {
  display: flex; flex-wrap: wrap; gap: 8px; margin: 0 20px 14px;
}
.hint-item {
  display: flex; align-items: center; gap: 4px;
  font-size: 11px; color: var(--text-light);
  padding: 4px 10px; background: rgba(248,164,184,0.06); border-radius: 8px;
}

.set-field {
  display: flex; align-items: center; gap: 10px; margin: 0 20px 10px;
  padding: 12px 14px; background: rgba(248,164,184,0.04); border-radius: 14px;
  border: 1px solid rgba(248,164,184,0.08);
}
.set-label {
  width: 72px; padding: 8px 10px; border: 1.5px solid rgba(248,164,184,0.15); border-radius: 10px;
  font-family: inherit; font-size: 14px; background: #fff; color: var(--text); outline: none;
  transition: border-color 0.2s;
}
.set-label:focus { border-color: var(--pink); }

.set-time {
  flex: 1; padding: 8px 12px; border: 1.5px solid rgba(248,164,184,0.15); border-radius: 10px;
  font-family: inherit; font-size: 14px; background: #fff; color: var(--text); outline: none;
  transition: border-color 0.2s;
}
.set-time:focus { border-color: var(--pink); }

.set-check {
  position: relative; cursor: pointer; flex-shrink: 0;
}
.set-check input { opacity: 0; position: absolute; }
.checkmark {
  display: block; width: 22px; height: 22px; border-radius: 6px;
  border: 2px solid rgba(248,164,184,0.3); background: #fff;
  transition: all 0.2s;
}
.set-check input:checked + .checkmark {
  background: var(--pink); border-color: var(--pink);
}
.set-check input:checked + .checkmark::after {
  content: ''; position: absolute; left: 7px; top: 3px;
  width: 5px; height: 10px; border: solid #fff; border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.set-del {
  width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid rgba(248,164,184,0.2);
  background: none; color: var(--text-light); cursor: pointer;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  transition: all 0.2s;
}
.set-del:active { background: var(--pink-light); border-color: var(--pink); color: var(--pink); }

.add-btn {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  width: calc(100% - 40px); margin: 12px 20px 0; padding: 12px;
  border: 2px dashed rgba(248,164,184,0.2); border-radius: 14px;
  background: none; font-family: inherit; font-size: 14px; color: var(--text-light);
  cursor: pointer; transition: all 0.2s;
}
.add-btn:active { background: rgba(248,164,184,0.04); border-color: var(--pink); }

.save-btn {
  width: calc(100% - 40px); margin: 10px 20px 20px; padding: 13px;
  border: none; border-radius: 14px; font-family: inherit;
  font-size: 15px; cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, var(--peach), var(--peach-light));
  color: var(--text); box-shadow: 0 3px 12px rgba(255,212,184,0.3);
  letter-spacing: 1px;
}
.save-btn:active { transform: scale(0.96); }

.backup-card { padding: 0 0 20px; }
.backup-btn {
  width: calc(100% - 40px); margin: 0 20px 12px; padding: 13px;
  border: none; border-radius: 16px; font-family: inherit; font-size: 15px; cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, var(--mint), var(--mint-light));
  color: var(--text); box-shadow: 0 3px 12px rgba(184,232,208,0.3);
  letter-spacing: 1px;
}
.backup-btn:active { transform: scale(0.96); }
.backup-btn:disabled { opacity: 0.5; }
.backup-msg {
  font-size: 12px; line-height: 1.6; margin: 0 20px; padding: 10px 14px;
  border-radius: 12px; background: rgba(248,164,184,0.06);
  color: var(--text); word-break: break-all;
}
</style>
