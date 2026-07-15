<template>
  <div class="stats-view">
    <van-nav-bar title="统计" />
    
    <div class="container">
      <van-radio-group v-model="range" direction="horizontal" @change="fetchStats">
        <van-radio name="week">本周</van-radio>
        <van-radio name="month">本月</van-radio>
      </van-radio-group>
      
      <van-cell-group inset style="margin-top: 16px">
        <van-cell title="完成率" :value="`${stats.overall}%`" />
        <van-cell title="已完成" :value="`${stats.done} / ${stats.total}`" />
      </van-cell-group>
      
      <div class="chart-container" v-if="stats.daily?.length">
        <div class="chart-title">每日打卡情况</div>
        <div class="chart">
          <div
            v-for="day in stats.daily"
            :key="day.date"
            class="chart-bar"
          >
            <div class="bar" :style="{ height: `${day.rate}%` }"></div>
            <div class="label">{{ day.date.slice(-2) }}</div>
          </div>
        </div>
      </div>
      
      <van-button
        type="primary"
        block
        style="margin-top: 16px"
        @click="analyzeAI"
        :loading="analyzing"
      >
        AI 分析
      </van-button>
      
      <div class="ai-report" v-if="aiReport">
        <div class="report-title">AI 分析报告</div>
        <div class="report-content" v-html="aiReport"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsApi, aiApi } from '../api'

const range = ref('week')
const stats = ref({ daily: [], overall: 0, total: 0, done: 0 })
const analyzing = ref(false)
const aiReport = ref('')

const fetchStats = async () => {
  stats.value = await statsApi.get(range.value)
}

const analyzeAI = async () => {
  analyzing.value = true
  try {
    const result = await aiApi.analyze(range.value)
    aiReport.value = result.content || result.fallback || result.error
  } finally {
    analyzing.value = false
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.stats-view {
  min-height: 100vh;
  background: var(--bg);
}

.container {
  max-width: 480px;
  margin: 0 auto;
  padding: 16px;
}

.chart-container {
  background: rgba(255, 255, 255, 0.88);
  border-radius: 20px;
  padding: 16px;
  margin-top: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
  text-align: center;
}

.chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 120px;
}

.chart-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bar {
  width: 20px;
  background: linear-gradient(to top, var(--pink), var(--pink-light));
  border-radius: 10px 10px 0 0;
  transition: height 0.3s;
}

.label {
  font-size: 12px;
  margin-top: 8px;
  color: var(--text-light);
}

.ai-report {
  background: rgba(255, 255, 255, 0.88);
  border-radius: 20px;
  padding: 16px;
  margin-top: 16px;
}

.report-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 12px;
}

.report-content {
  font-size: 14px;
  line-height: 1.6;
}
</style>
