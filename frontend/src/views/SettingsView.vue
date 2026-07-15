<template>
  <div class="settings-view">
    <van-nav-bar title="设置" />
    
    <div class="container">
      <div class="tips">
        <van-icon name="info-o" /> 点击项目名称可编辑，拖动可排序
      </div>
      
      <van-cell-group inset>
        <van-cell
          v-for="schedule in schedules"
          :key="schedule.id"
          :title="schedule.label"
          :value="getTime(schedule)"
        >
          <template #right-icon>
            <van-switch
              v-model="schedule.enabled"
              size="20"
              @change="toggleEnabled(schedule)"
            />
          </template>
        </van-cell>
      </van-cell-group>
      
      <van-button
        type="primary"
        block
        style="margin-top: 16px"
        @click="showAdd = true"
      >
        添加新项目
      </van-button>
      
      <van-cell-group inset style="margin-top: 16px" v-if="schedules.length">
        <van-cell
          v-for="schedule in schedules"
          :key="schedule.id + '-edit'"
          :title="schedule.label"
          is-link
          @click="editSchedule(schedule)"
        />
      </van-cell-group>
    </div>
    
    <van-dialog
      v-model:show="showAdd"
      title="添加作息项目"
      show-cancel-button
      @confirm="addSchedule"
    >
      <van-field v-model="newLabel" label="名称" placeholder="请输入名称" />
      <van-field v-model="newHour" label="小时" type="digit" placeholder="0-23" />
      <van-field v-model="newMinute" label="分钟" type="digit" placeholder="0-59" />
    </van-dialog>
    
    <van-dialog
      v-model:show="showEdit"
      title="编辑作息项目"
      show-cancel-button
      @confirm="updateSchedule"
    >
      <van-field v-model="editLabel" label="名称" placeholder="请输入名称" />
      <van-field v-model="editHour" label="小时" type="digit" placeholder="0-23" />
      <van-field v-model="editMinute" label="分钟" type="digit" placeholder="0-59" />
    </van-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { showToast } from 'vant'

const scheduleStore = useScheduleStore()
const schedules = ref([])

const showAdd = ref(false)
const showEdit = ref(false)

const newLabel = ref('')
const newHour = ref('8')
const newMinute = ref('0')

const editId = ref('')
const editLabel = ref('')
const editHour = ref('')
const editMinute = ref('')

const getTime = (schedule) => {
  return `${schedule.hour.toString().padStart(2, '0')}:${schedule.minute.toString().padStart(2, '0')}`
}

const toggleEnabled = async (schedule) => {
  await scheduleStore.updateSchedule(schedule.id, { enabled: schedule.enabled })
  showToast('已更新')
}

const addSchedule = async () => {
  if (!newLabel.value) {
    showToast('请输入名称')
    return
  }
  
  const id = newLabel.value.toLowerCase().replace(/\s+/g, '_')
  await scheduleStore.addSchedule({
    id,
    label: newLabel.value,
    hour: parseInt(newHour.value) || 8,
    minute: parseInt(newMinute.value) || 0,
    enabled: true
  })
  
  newLabel.value = ''
  newHour.value = '8'
  newMinute.value = '0'
  showToast('添加成功')
  await loadSchedules()
}

const editSchedule = (schedule) => {
  editId.value = schedule.id
  editLabel.value = schedule.label
  editHour.value = schedule.hour.toString()
  editMinute.value = schedule.minute.toString()
  showEdit.value = true
}

const updateSchedule = async () => {
  if (!editLabel.value) {
    showToast('请输入名称')
    return
  }
  
  await scheduleStore.updateSchedule(editId.value, {
    label: editLabel.value,
    hour: parseInt(editHour.value) || 8,
    minute: parseInt(editMinute.value) || 0
  })
  
  showToast('更新成功')
  await loadSchedules()
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

.container {
  max-width: 480px;
  margin: 0 auto;
  padding: 16px;
}

.tips {
  background: rgba(255, 255, 255, 0.88);
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--text-light);
  text-align: center;
}
</style>
