<template>
  <div class="weather-view">
    <div class="weather-grid">
      <div class="weather-card" v-for="city in cities" :key="city.id">
        <div class="city-header">
          <div class="city-name">{{ city.name }} {{ city.id === 'xian' ? '🏯' : '🧊' }}</div>
          <div class="city-now">现在</div>
        </div>
        <div class="temp-main">
          <span class="weather-icon">{{ city.emoji }}</span>
          <div class="temp-num">{{ Math.round(city.temperature) }}<small>°C</small></div>
          <div class="weather-desc">{{ city.weather_desc }}</div>
          <div class="temp-range" v-if="city.temp_max && city.temp_min">
            ↑ {{ Math.round(city.temp_max) }}° ↓ {{ Math.round(city.temp_min) }}°
          </div>
        </div>
        <div class="weather-detail">
          <span>体感<br><span class="val">{{ Math.round(city.apparent_temperature) }}°</span></span>
          <span>湿度<br><span class="val">{{ city.humidity }}%</span></span>
          <span>风速<br><span class="val">{{ Math.round(city.wind_speed) }}km/h</span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { weatherApi } from '../api'

const updateTip = inject('updateTip')
const cities = ref([])

const cityList = [
  { id: 'xian', name: '西安' },
  { id: 'harbin', name: '哈尔滨' }
]

const fetchWeather = async () => {
  try {
    const results = await Promise.all(
      cityList.map(async (city) => {
        const data = await weatherApi.get(city.id)
        return { ...data, id: city.id }
      })
    )
    cities.value = results
    updateTip('🌤', '西安和哈尔滨的天气都查好啦 ☀️')
  } catch {
    updateTip('🥺', '天气加载失败了，晚点再试试吧')
  }
}

onMounted(fetchWeather)
</script>

<style scoped>
.weather-view {
  min-height: 100vh;
  background: var(--bg);
}

.weather-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.weather-card {
  background: var(--card); backdrop-filter: blur(12px);
  border-radius: var(--radius); box-shadow: var(--shadow);
  border: 1.5px solid rgba(255,182,193,0.15); overflow: hidden;
  transition: transform 0.2s;
}
.weather-card:active { transform: scale(0.97); }

.city-header {
  padding: 14px 14px 10px; text-align: center;
  background: linear-gradient(135deg, rgba(255,182,193,0.15), rgba(212,165,255,0.1));
  border-bottom: 1px solid rgba(255,182,193,0.1);
}
.city-name { font-size: 15px; font-weight: 400; color: var(--text); letter-spacing: 1px; }
.city-now { font-size: 11px; color: var(--text-light); margin-top: 2px; }

.temp-main { text-align: center; padding: 12px 14px 6px; }
.weather-icon { font-size: 32px; margin: 4px 0; display: block; }
.temp-num { font-size: 36px; font-weight: 400; color: var(--text); line-height: 1; }
.temp-num small { font-size: 16px; color: var(--text-light); }
.weather-desc { font-size: 13px; color: var(--text-light); margin-top: 4px; }
.temp-range { font-size: 13px; color: var(--text-light); margin-top: 4px; }

.weather-detail {
  display: grid; grid-template-columns: 1fr 1fr; gap: 6px;
  padding: 8px 14px 14px; font-size: 11px; color: var(--text-light);
}
.weather-detail span { text-align: center; }
.weather-detail .val { font-size: 13px; color: var(--text); font-weight: 400; }
</style>
