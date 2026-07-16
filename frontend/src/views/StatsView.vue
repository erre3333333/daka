<template>
  <div class="stats-view">
    <div class="card chart-wrap">
      <div class="card-header">
        <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="var(--pink)" stroke-width="2">
          <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <div>
          <div class="title">本周规律趋势</div>
          <div class="subtitle">完成率 {{ stats.overall }}% · 共 {{ stats.done }} 项</div>
        </div>
      </div>
      
      <div class="empty-state" v-if="!stats.daily.length">
        <div class="empty-icon">
          <svg viewBox="0 0 48 48" fill="none" stroke="var(--pink-light)" stroke-width="2">
            <rect x="6" y="10" width="36" height="28" rx="4"/>
            <path d="M14 22h20M14 30h12"/>
          </svg>
        </div>
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
      <div class="card-header">
        <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="var(--lavender)" stroke-width="2">
          <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <div>
          <div class="title">AI 健康分析</div>
          <div class="subtitle">基于本周打卡数据的贴心分析</div>
        </div>
      </div>
      <button class="gen-btn" @click="generateReport" :disabled="loading">
        <span v-if="loading" class="loading-dots">分析中</span>
        <span v-else>生成专属周报 💕</span>
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

const formatDate = (dateStr) => dateStr.slice(5).replace('-', '/')

const getBarHeight = (rate) => {
  const maxRate = Math.max(...stats.value.daily.map(d => d.rate), 1)
  return Math.max(4, (rate / maxRate) * 100)
}

const fetchStats = async () => { stats.value = await statsApi.get('week') }

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
.stats-view { position: relative; }

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

.empty-state {
  text-align: center; padding: 40px 20px; color: var(--text-light);
}
.empty-icon {
  width: 64px; height: 64px; margin: 0 auto 14px;
  background: var(--pink-light); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.empty-icon svg { width: 32px; height: 32px; }
.empty-state p { font-size: 14px; line-height: 1.9; }

.chart { display: flex; align-items: flex-end; gap: 8px; height: 140px; padding: 0 20px 20px; }
.chart-bar { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.chart-bar .bar {
  width: 100%; border-radius: 8px 8px 4px 4px;
  background: linear-gradient(180deg, var(--pink-light), var(--pink));
  min-height: 4px; transition: height 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.chart-bar .bar-label { font-size: 10px; color: var(--text-light); white-space: nowrap; }
.chart-bar .bar-pct { font-size: 11px; color: var(--pink); }

.report-wrap { padding: 0 0 20px; }
.gen-btn {
  width: calc(100% - 40px); margin: 0 20px 14px; padding: 13px; border: none; border-radius: 16px;
  font-family: inherit; font-size: 15px; cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, var(--pink), var(--lavender));
  color: #fff; box-shadow: 0 4px 16px rgba(248,164,184,0.3);
  letter-spacing: 1px;
}
.gen-btn:active { transform: scale(0.96); }
.gen-btn:disabled { opacity: 0.5; }

.loading-dots::after {
  content: ''; animation: dots 1.4s infinite;
}
@keyframes dots {
  0% { content: ''; } 25% { content: '.'; } 50% { content: '..'; } 75% { content: '...'; }
}

.report-content {
  font-size: 14px; line-height: 2; color: var(--text); white-space: pre-wrap;
  margin: 0 20px; padding: 16px; border-radius: 14px;
  background: linear-gradient(135deg, rgba(248,164,184,0.06), rgba(212,191,255,0.06));
  border-left: 3px solid var(--pink);
}
</style>
