<template>
  <div class="weather-view">
    <van-nav-bar title="天气" />
    
    <div class="container">
      <van-loading v-if="loading" style="text-align: center; padding: 40px" />
      
      <template v-else>
        <div class="weather-card" v-for="city in cities" :key="city.id">
          <div class="city-name">{{ city.name }}</div>
          <div class="weather-main">
            <span class="emoji">{{ city.emoji }}</span>
            <span class="temp">{{ city.temperature }}°</span>
          </div>
          <div class="weather-desc">{{ city.weather_desc }}</div>
          <div class="weather-detail">
            <span>体感 {{ city.apparent_temperature }}°</span>
            <span>湿度 {{ city.humidity }}%</span>
            <span>风速 {{ city.wind_speed }}km/h</span>
          </div>
          <div class="temp-range">
            <span>↑ {{ city.temp_max }}°</span>
            <span>↓ {{ city.temp_min }}°</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { weatherApi } from '../api'

const loading = ref(true)
const cities = ref([])

const cityList = [
  { id: 'xian', name: '西安' },
  { id: 'harbin', name: '哈尔滨' }
]

const fetchWeather = async () => {
  loading.value = true
  try {
    const results = await Promise.all(
      cityList.map(async (city) => {
        const data = await weatherApi.get(city.id)
        return { ...data, id: city.id }
      })
    )
    cities.value = results
  } finally {
    loading.value = false
  }
}

onMounted(fetchWeather)
</script>

<style scoped>
.weather-view {
  min-height: 100vh;
  background: var(--bg);
}

.container {
  max-width: 480px;
  margin: 0 auto;
  padding: 16px;
}

.weather-card {
  background: linear-gradient(135deg, #FFB5C2 0%, #D4A5FF 100%);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 16px;
  color: #fff;
}

.city-name {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 12px;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.emoji {
  font-size: 48px;
}

.temp {
  font-size: 48px;
  font-weight: 300;
}

.weather-desc {
  font-size: 16px;
  margin-top: 8px;
}

.weather-detail {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  font-size: 14px;
  opacity: 0.9;
}

.temp-range {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  font-size: 14px;
  opacity: 0.8;
}
</style>
