<template>
  <div class="weather-view">
    <div class="weather-grid">
      <div class="weather-card" v-for="city in cities" :key="city.id">
        <div class="city-header" :class="city.id">
          <div class="city-name">{{ city.city }}</div>
          <div class="city-now">实时</div>
        </div>
        <div class="temp-main">
          <div class="weather-emoji">{{ city.emoji }}</div>
          <div class="temp-num">{{ Math.round(city.temperature) }}<small>°</small></div>
          <div class="weather-desc">{{ city.weather_desc }}</div>
          <div class="temp-range" v-if="city.temp_max && city.temp_min">
            <span class="temp-up">↑ {{ Math.round(city.temp_max) }}°</span>
            <span class="temp-down">↓ {{ Math.round(city.temp_min) }}°</span>
          </div>
        </div>
        <div class="weather-detail">
          <div class="detail-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="var(--text-light)" stroke-width="1.5" width="16" height="16">
              <path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/>
            </svg>
            <span class="val">{{ Math.round(city.apparent_temperature) }}°</span>
          </div>
          <div class="detail-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="var(--text-light)" stroke-width="1.5" width="16" height="16">
              <path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/>
            </svg>
            <span class="val">{{ city.humidity }}%</span>
          </div>
          <div class="detail-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="var(--text-light)" stroke-width="1.5" width="16" height="16">
              <path d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
            </svg>
            <span class="val">{{ Math.round(city.wind_speed) }}km/h</span>
          </div>
        </div>
      </div>
    </div>

    <div class="hourly-card" v-if="hourlyData.length">
      <div class="card-header">
        <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="var(--pink)" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
        </svg>
        <div>
          <div class="title">小时预报</div>
          <div class="subtitle">未来12小时温度与降水</div>
        </div>
      </div>
      <div class="city-tabs">
        <button class="city-tab" v-for="c in cities" :key="c.city" :class="{ active: chartCity === c.city }" @click="chartCity = c.city">{{ c.city }}</button>
      </div>
      <div class="scroll-wrap">
        <div class="hourly-scroll">
          <div class="hour-item" v-for="(h, i) in hourlyData" :key="i">
            <div class="h-time">{{ h.time }}</div>
            <div class="h-icon">{{ wmoIcon(h.code, h.pop) }}</div>
            <div class="h-pop" v-if="h.pop > 0">{{ h.pop }}%</div>
            <div class="h-text" v-else></div>
            <div class="h-temp">{{ Math.round(h.temp) }}°</div>
          </div>
        </div>
        <div class="scroll-fade"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { weatherApi } from '../api'

const updateTip = inject('updateTip')
const cities = ref([])
const chartCity = ref('西安')

const cityList = [
  { id: 'xian', name: '西安' },
  { id: 'harbin', name: '哈尔滨' }
]

const activeCity = computed(() => cities.value.find(c => c.city === chartCity.value))
const hourlyData = computed(() => activeCity.value?.hourly || [])

const WMO = {
  0: '☀️', 1: '🌤', 2: '⛅', 3: '☁️', 45: '🌫', 48: '🌫',
  51: '🌦', 53: '🌦', 55: '🌦', 61: '🌧', 63: '🌧', 65: '🌧',
  66: '🌧', 67: '🌧', 71: '🌨', 73: '🌨', 75: '❄️', 77: '🌨',
  80: '🌦', 81: '🌧', 82: '🌧', 83: '🌨', 84: '🌨',
  95: '⛈', 96: '⛈', 99: '⛈'
}
const RAIN_CODES = new Set([51,53,55,61,63,65,66,67,71,73,75,77,80,81,82,83,84,95,96,99])

const wmoIcon = (code, pop) => {
  if (pop > 0 && !RAIN_CODES.has(code)) return '🌦'
  return WMO[code] || '☀️'
}

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
.weather-view { position: relative; }
.weather-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.weather-card {
  background: var(--card); backdrop-filter: blur(16px);
  border-radius: var(--radius); box-shadow: var(--shadow);
  border: 1px solid rgba(248,164,184,0.12); overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.weather-card:active { transform: scale(0.97); box-shadow: var(--shadow-hover); }
.city-header { padding: 14px 14px 10px; text-align: center; border-bottom: 1px solid rgba(248,164,184,0.08); }
.city-header.xian { background: linear-gradient(135deg, rgba(248,164,184,0.12), rgba(212,191,255,0.08)); }
.city-header.harbin { background: linear-gradient(135deg, rgba(184,232,208,0.12), rgba(212,191,255,0.08)); }
.city-name { font-size: 15px; font-weight: 400; color: var(--text); letter-spacing: 1px; }
.city-now { font-size: 11px; color: var(--text-light); margin-top: 2px; }
.temp-main { text-align: center; padding: 16px 14px 8px; }
.weather-emoji { font-size: 36px; margin-bottom: 4px; }
.temp-num { font-size: 40px; font-weight: 400; color: var(--text); line-height: 1; }
.temp-num small { font-size: 18px; color: var(--text-light); }
.weather-desc { font-size: 13px; color: var(--text-light); margin-top: 6px; }
.temp-range { display: flex; gap: 10px; justify-content: center; margin-top: 6px; font-size: 12px; }
.temp-up { color: var(--pink); }
.temp-down { color: var(--lavender); }
.weather-detail { display: flex; justify-content: space-around; padding: 10px 14px 14px; }
.detail-item { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 11px; color: var(--text-light); }
.detail-item .val { font-size: 13px; color: var(--text); font-weight: 400; }

.hourly-card {
  background: var(--card); backdrop-filter: blur(16px);
  border-radius: var(--radius); box-shadow: var(--shadow);
  border: 1px solid rgba(248,164,184,0.12); overflow: hidden;
  margin-top: 14px; padding: 0 0 12px;
}
.card-header { display: flex; align-items: center; gap: 12px; padding: 18px 20px 8px; }
.card-icon { width: 24px; height: 24px; flex-shrink: 0; }
.title { font-size: 15px; font-weight: 400; letter-spacing: 0.5px; }
.subtitle { font-size: 11px; color: var(--text-light); margin-top: 1px; }
.city-tabs { display: flex; gap: 8px; padding: 8px 20px 12px; }
.city-tab {
  padding: 4px 16px; border: 1.5px solid rgba(248,164,184,0.2); border-radius: 14px;
  background: none; font-family: inherit; font-size: 13px; color: var(--text-light); cursor: pointer;
}
.city-tab.active { background: var(--pink-light); border-color: var(--pink); color: var(--pink); }

.scroll-wrap { position: relative; }
.hourly-scroll {
  display: flex; gap: 0; overflow-x: auto; padding: 4px 16px 12px;
  scrollbar-width: thin; scrollbar-color: var(--pink) transparent;
  -webkit-overflow-scrolling: touch;
}
.hourly-scroll::-webkit-scrollbar { height: 3px; }
.hourly-scroll::-webkit-scrollbar-thumb { background: var(--pink); border-radius: 3px; }
.hour-item {
  flex: 0 0 64px; display: flex; flex-direction: column;
  align-items: center; gap: 4px; padding: 8px 2px; position: relative;
}
.h-time { font-size: 12px; color: var(--text-light); font-weight: 400; }
.h-icon { font-size: 22px; line-height: 1; margin: 2px 0; }
.h-pop { font-size: 10px; color: #7EC8E3; font-weight: 400; min-height: 14px; }
.h-text { min-height: 14px; }
.h-temp { font-size: 16px; font-weight: 500; color: var(--text); line-height: 1.2; }
.scroll-fade {
  position: absolute; right: 0; top: 0; bottom: 16px; width: 32px;
  background: linear-gradient(90deg, transparent, var(--bg));
  pointer-events: none;
}
</style>
