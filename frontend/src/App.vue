<template>
  <div class="app">
    <!-- 头部 -->
    <div class="header">
      <div class="header-deco-left">✿</div>
      <div class="header-deco-right">❀</div>
      <div class="greeting">{{ greeting }}</div>
      <div class="rate-wrap">
        <div class="tip-text">{{ tipIcon }} {{ tipText }}</div>
        <div class="rate-row">
          <span>今日完成</span>
          <div class="rate-bar">
            <div class="rate-fill" :style="{ width: completionRate + '%' }"></div>
          </div>
          <span class="num">{{ completionRate }}%</span>
        </div>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="container">
      <router-view />
    </div>

    <!-- 底部导航 -->
    <div class="toolbar">
      <button class="tab" :class="{ active: activeTab === 'checkin' }" @click="switchTab('checkin')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
        </svg>
        <span>今日</span>
      </button>
      <button class="tab" :class="{ active: activeTab === 'stats' }" @click="switchTab('stats')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <span>统计</span>
      </button>
      <button class="tab" :class="{ active: activeTab === 'weather' }" @click="switchTab('weather')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
        </svg>
        <span>天气</span>
      </button>
      <button class="tab" :class="{ active: activeTab === 'settings' }" @click="switchTab('settings')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
        <span>设置</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, provide, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useScheduleStore } from './stores/schedule'
import { useCheckinStore } from './stores/checkin'

const router = useRouter()
const route = useRoute()
const scheduleStore = useScheduleStore()
const checkinStore = useCheckinStore()

const now = ref(new Date())
const activeTab = ref('checkin')

const tabMap = { '/': 'checkin', '/stats': 'stats', '/weather': 'weather', '/settings': 'settings' }

watch(() => route.path, (path) => {
  activeTab.value = tabMap[path] || 'checkin'
}, { immediate: true })
const tipIcon = ref('🌸')
const tipText = ref('今天也要元气满满哦！')
const completionRate = computed(() => {
  const enabled = scheduleStore.schedules.filter(s => s.enabled !== false).length
  const done = checkinStore.checkins.filter(c => c.status === 'done').length
  return enabled > 0 ? Math.round(done / enabled * 100) : 0
})

const greeting = computed(() => {
  const hour = now.value.getHours()
  if (hour < 6) return '夜深了，该睡啦 💤'
  if (hour < 9) return '早上好呀 ☀️ 新的一天加油'
  if (hour < 12) return '上午好 💕 元气满满'
  if (hour < 14) return '中午好呀 🍚 记得吃饭'
  if (hour < 18) return '下午好 🌸 加油哦'
  if (hour < 21) return '傍晚好 💖 放松一下吧'
  return '晚安 🌙 要早点休息哦'
})

const tips = [
  { icon: '💖', text: '和你在一起的每一天都是礼物' },
  { icon: '☀️', text: '醒来想到你，空气都是甜的' },
  { icon: '🌸', text: '你比春天还温柔' },
  { icon: '🌟', text: '我的世界因为有你会发光' },
  { icon: '🎀', text: '你这么可爱，一定是吃可爱多长大的' },
  { icon: '💝', text: '心都被你填满了' },
  { icon: '🦋', text: '你一出现，连风都是甜的' },
  { icon: '🍯', text: '你是生活给我的糖' },
  { icon: '🌷', text: '在我眼里你永远最好看' },
  { icon: '✨', text: '你的存在就是我的小确幸' },
]

const tabTips = {
  checkin: [
    { icon: '💪', text: '今天也要元气满满哦！' },
    { icon: '💖', text: '每一步打卡都是爱自己的表现' },
    { icon: '✨', text: '坚持就是最棒的礼物' },
  ],
  stats: [
    { icon: '📊', text: '看看你的进步轨迹吧' },
    { icon: '🌟', text: '每一份努力都值得被记录' },
    { icon: '💪', text: '数据见证你的成长' },
  ],
  weather: [
    { icon: '🌤', text: '今天出门记得看天气哦' },
    { icon: '☀️', text: '天气好就出去走走吧' },
    { icon: '🌈', text: '不管什么天气都要开心' },
  ],
  settings: [
    { icon: '⚙️', text: '定制属于你的专属计划' },
    { icon: '🎀', text: '调整一下，让自己更舒服' },
    { icon: '💫', text: '好的计划是成功的一半' },
  ],
}

const switchTab = (tab) => {
  activeTab.value = tab
  router.push(`/${tab === 'checkin' ? '' : tab}`)
  const list = tabTips[tab] || tabTips.checkin
  const t = list[Math.floor(Math.random() * list.length)]
  tipIcon.value = t.icon
  tipText.value = t.text
}

let timer = null

onMounted(async () => {
  await scheduleStore.fetchSchedules()
  const date = now.value.toISOString().slice(0, 10)
  await checkinStore.fetchCheckins(date)

  const randomTip = tips[Math.floor(Math.random() * tips.length)]
  tipIcon.value = randomTip.icon
  tipText.value = randomTip.text

  timer = setInterval(() => {
    now.value = new Date()
  }, 60000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

provide('completionRate', completionRate)
provide('updateTip', (icon, text) => {
  tipIcon.value = icon
  tipText.value = text
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
:root {
  --pink: #F8A4B8;
  --pink-light: #FFD6E0;
  --pink-dark: #E8899E;
  --lavender: #D4BFFF;
  --lavender-light: #EDE4FF;
  --mint: #B8E8D0;
  --mint-light: #E0F5EB;
  --peach: #FFD4B8;
  --peach-light: #FFE8D8;
  --cream: #FFF5EC;
  --bg: #FFF9FB;
  --card: rgba(255,255,255,0.92);
  --text: #5A3D4A;
  --text-light: #B8929E;
  --shadow: 0 4px 20px rgba(248,164,184,0.12);
  --shadow-hover: 0 8px 32px rgba(248,164,184,0.18);
  --radius: 22px;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}
body {
  font-family: 'ZCOOL KuaiLe', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif;
  background: linear-gradient(170deg, #FFF5F7 0%, #FFF0F5 25%, #F8F0FF 50%, #F0F8F4 75%, #FFF8F0 100%);
  background-attachment: fixed;
  color: var(--text); height: 100vh; overflow: hidden;
}
html, body, #app { height: 100%; margin: 0; padding: 0; }
</style>

<style scoped>
.app {
  display: flex; flex-direction: column;
  height: 100vh; overflow: hidden;
}

.header {
  flex-shrink: 0;
  background: linear-gradient(135deg, #FFD6E0 0%, #F8A4B8 25%, #D4BFFF 55%, #B8E8D0 85%, #FFD4B8 100%);
  color: #fff; padding: 32px 20px 28px; text-align: center; position: relative; z-index: 1;
  border-radius: 0 0 32px 32px;
  box-shadow: 0 8px 32px rgba(248,164,184,0.25);
}
.header-deco-left, .header-deco-right {
  position: absolute; top: 10px; font-size: 18px; opacity: 0.45;
}
.header-deco-left { left: 14px; }
.header-deco-right { right: 14px; }
.header .title {
  font-size: 28px; font-weight: 400; margin-bottom: 6px; letter-spacing: 2px;
  color: #D44E7A;
  text-shadow: 0 1px 8px rgba(255,255,255,0.6), 0 2px 4px rgba(212,78,122,0.15);
  animation: titleBounce 3s ease-in-out infinite;
  font-family: 'Liu Jian Mao Cao', 'ZCOOL KuaiLe', 'STKaiti', 'KaiTi', 'SimKai', cursive, serif;
}
@keyframes titleBounce {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-2px) rotate(-1deg); }
  75% { transform: translateY(-2px) rotate(1deg); }
}
.header .greeting {
  font-size: 13px; opacity: 0.92; letter-spacing: 1.5px; margin-bottom: 2px;
}
.header .rate-wrap {
  display: flex; flex-direction: column; align-items: center; gap: 8px; margin-top: 14px;
  background: rgba(255,255,255,0.35); backdrop-filter: blur(12px);
  border-radius: 24px; padding: 12px 20px; font-size: 13px;
  border: 1px solid rgba(255,255,255,0.4);
}
.header .rate-wrap .tip-text {
  font-size: 16px; opacity: 1; letter-spacing: 0.5px;
  color: #4FC3F7; font-weight: 400;
}
.header .rate-wrap .rate-row {
  display: flex; align-items: center; gap: 10px; width: 100%;
}
.header .rate-wrap .rate-row span:first-child { font-size: 13px; white-space: nowrap; }
.rate-bar {
  flex: 1; height: 8px; background: rgba(255,255,255,0.35); border-radius: 10px; overflow: hidden;
}
.rate-fill {
  height: 100%; background: #fff; border-radius: 10px;
  transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 0 8px rgba(255,255,255,0.5);
}
.header .rate-wrap .num {
  font-size: 18px; font-weight: 400; min-width: 40px; text-align: right;
  text-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.container {
  flex: 1;
  max-width: 480px; margin: 0 auto; padding: 16px;
  position: relative; z-index: 1;
  width: 100%;
  overflow-y: auto; overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 80px;
  scrollbar-width: none;
}
.container::-webkit-scrollbar { display: none; }

.toolbar {
  position: fixed; bottom: 0; left: 6px; right: 6px;
  background: rgba(255,255,255,0.92); backdrop-filter: blur(20px);
  box-shadow: 0 -4px 24px rgba(248,164,184,0.1);
  display: flex; padding: 6px 8px calc(6px + var(--safe-bottom)); gap: 4px;
  z-index: 20; align-items: center;
  border-radius: 24px 24px 0 0;
  border-top: 1px solid rgba(248,164,184,0.12);
}
.toolbar .tab {
  flex: 1; text-align: center; padding: 8px 4px; border: none; background: none;
  font-family: inherit; font-size: 11px; color: var(--text-light); cursor: pointer;
  border-radius: 16px; transition: all 0.25s ease;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
}
.toolbar .tab .tab-svg {
  width: 22px; height: 22px; transition: all 0.25s ease;
}
.toolbar .tab.active { color: var(--pink); background: rgba(248,164,184,0.1); }
.toolbar .tab.active .tab-svg { animation: tabBounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes tabBounce {
  0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1.05); }
}
</style>
