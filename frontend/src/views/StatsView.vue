<template>
  <div class="stats-view">
    <div class="card chart-wrap">
      <div class="title">📊 本周规律趋势</div>
      <div class="subtitle">完成率 {{ stats.overall }}% · 共 {{ stats.done }} 项</div>
      
      <div class="empty-state" v-if="!stats.daily.length">
        <div class="icon">📊</div>
        <p>还没有打卡数据<br>今天开始记录吧 💕</p>
      </div>

      <div class="chart" v-else>
        <div class="chart-bar" v-for="d in stats.daily" :key="d.date">
          <div class="bar-pct">{{ d.rate }}%</div>
          <div class="bar" :style="{ height: getBarHeight(d.rate) + '%' }"></div>
          <div class="bar-label">{{ formatDate(d.date) }}</div>
        </div>
      </div>
    </div>

    <div class="card report-wrap">
      <div class="title">🤖 AI 健康分析</div>
      <div class="subtitle">基于本周打卡数据的贴心分析</div>
      <button class="gen-btn" @click="generateReport" :disabled="loading">
        {{ loading ? '⏳ 分析中...' : '💕 生成专属周报' }}
      </button>
      <div class="report-content" v-if="reportContent">{{ reportContent }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { statsApi, aiApi } from '../api'

const updateTip = inject('updateTip')

const stats = ref({ overall: 0, done: 0, daily: [] })
const reportContent = ref('')
const loading = ref(false)

const formatDate = (dateStr) => {
  return dateStr.slice(5).replace('-', '/')
}

const getBarHeight = (rate) => {
  const maxRate = Math.max(...stats.value.daily.map(d => d.rate), 1)
  return Math.max(4, (rate / maxRate) * 100)
}

const fetchStats = async () => {
  stats.value = await statsApi.get('week')
}

const generateReport = async () => {
  loading.value = true
  reportContent.value = ''
  try {
    const result = await aiApi.analyze('week')
    reportContent.value = result.content || result.fallback || 'AI 暂时不在线，晚点再试试哦 🥺'
  } catch {
    reportContent.value = '哎呀，出了点小问题 🥺 晚点再试试吧'
  }
  loading.value = false
}

onMounted(async () => {
  await fetchStats()
  updateTip('📊', `本周完成 ${stats.value.done} 项 · 规律率 ${stats.value.overall}%`)
})
</script>

<style scoped>
.stats-view {
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

.chart-wrap { padding: 20px; }
.chart-wrap .title { font-size: 16px; font-weight: 400; margin-bottom: 2px; letter-spacing: 1px; }
.chart-wrap .subtitle { font-size: 12px; color: var(--text-light); margin-bottom: 16px; }

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-light);
}
.empty-state .icon { font-size: 56px; margin-bottom: 12px; display: block; }
.empty-state p { font-size: 14px; line-height: 1.8; }

.chart { display: flex; align-items: flex-end; gap: 8px; height: 150px; padding: 0 4px; }
.chart-bar { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.chart-bar .bar {
  width: 100%; border-radius: 8px 8px 4px 4px;
  background: linear-gradient(180deg, var(--pink-light), var(--pink));
  min-height: 4px; transition: height 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}
.chart-bar .bar-label { font-size: 10px; color: var(--text-light); white-space: nowrap; }
.chart-bar .bar-pct { font-size: 12px; font-weight: 400; color: var(--pink); }

.report-wrap { padding: 20px; }
.report-wrap .title { font-size: 16px; font-weight: 400; margin-bottom: 2px; }
.report-wrap .subtitle { font-size: 12px; color: var(--text-light); margin-bottom: 14px; }

.gen-btn {
  width: 100%; padding: 14px; border: none; border-radius: 16px; font-family: inherit;
  font-size: 16px; font-weight: 400; cursor: pointer; margin-bottom: 14px;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, var(--pink), var(--pink-light));
  color: #fff; box-shadow: 0 4px 16px rgba(255,143,171,0.3);
  letter-spacing: 1px;
}
.gen-btn:active { transform: scale(0.95); }
.gen-btn:disabled { opacity: 0.5; }

.report-content {
  font-size: 14px; line-height: 2; color: var(--text); white-space: pre-wrap;
  background: rgba(255,182,193,0.06); border-radius: 14px; padding: 16px 18px;
  border-left: 3px solid var(--pink);
}
</style>
