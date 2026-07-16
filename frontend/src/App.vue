<template>
  <div class="app">
    <!-- 浮动装饰 -->
    <div class="floating-deco">
      <div class="deco">🌸</div><div class="deco">💕</div><div class="deco">✨</div>
      <div class="deco">🌷</div><div class="deco">💖</div><div class="deco">🌟</div>
      <div class="deco">🌺</div><div class="deco">💫</div><div class="deco">🦋</div>
      <div class="deco">🍭</div>
    </div>

    <!-- 头部 -->
    <div class="header">
      <div class="greeting">{{ greeting }}</div>
      <div class="name">宝宝 <span>💕</span></div>
      <div class="clock">
        <span id="clockH">{{ hours }}</span>
        <span class="clock-sep">:</span>
        <span id="clockM">{{ minutes }}</span>
      </div>
      <div class="rate-wrap">
        <span>今日完成</span>
        <span class="num">{{ completionRate }}%</span>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="container">
      <div class="tip-banner">
        <span class="tip-icon">{{ tipIcon }}</span>
        <span id="tipText">{{ tipText }}</span>
      </div>

      <router-view />
    </div>

    <!-- 底部导航 -->
    <div class="toolbar">
      <button class="tab" :class="{ active: activeTab === 'checkin' }" @click="switchTab('checkin')">
        <span class="tab-icon">📋</span> 今日
      </button>
      <button class="tab" :class="{ active: activeTab === 'stats' }" @click="switchTab('stats')">
        <span class="tab-icon">📊</span> 统计
      </button>
      <button class="tab" :class="{ active: activeTab === 'weather' }" @click="switchTab('weather')">
        <span class="tab-icon">🌤</span> 天气
      </button>
      <button class="tab" :class="{ active: activeTab === 'settings' }" @click="switchTab('settings')">
        <span class="tab-icon">⚙️</span> 设置
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useScheduleStore } from './stores/schedule'
import { useCheckinStore } from './stores/checkin'

const router = useRouter()
const scheduleStore = useScheduleStore()
const checkinStore = useCheckinStore()

const now = ref(new Date())
const activeTab = ref('checkin')
const tipIcon = ref('💪')
const tipText = ref('今天也要元气满满哦！')
const completionRate = computed(() => checkinStore.completionRate)

const hours = computed(() => now.value.getHours().toString().padStart(2, '0'))
const minutes = computed(() => now.value.getMinutes().toString().padStart(2, '0'))

const greeting = computed(() => {
  const hour = now.value.getHours()
  if (hour < 6) return '夜深了宝宝，该睡啦 💤'
  if (hour < 9) return '早上好呀 ☀️ 新的一天加油'
  if (hour < 12) return '上午好宝宝 💕 元气满满'
  if (hour < 14) return '中午好呀 🍚 记得吃饭'
  if (hour < 18) return '下午好宝宝 🌸 加油哦'
  if (hour < 21) return '傍晚好 💖 放松一下吧'
  return '晚安宝宝 🌙 要早点休息哦'
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

const switchTab = (tab) => {
  activeTab.value = tab
  router.push(`/${tab === 'checkin' ? '' : tab}`)
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
  }, 1000)
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
  --pink: #FF8FAB;
  --pink-light: #FFB5C2;
  --pink-dark: #E85D8A;
  --lavender: #D4A5FF;
  --mint: #A8E6CF;
  --peach: #FFD3B6;
  --cream: #FFF0E6;
  --bg: #FFF8FA;
  --card: rgba(255,255,255,0.88);
  --text: #5A3D4A;
  --text-light: #A88494;
  --shadow: 0 6px 28px rgba(255,107,157,0.1);
  --radius: 20px;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}
body {
  font-family: 'ZCOOL KuaiLe', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh; padding-bottom: 90px;
  overflow-x: hidden; overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
html { overflow-y: auto; }
</style>

<style scoped>
.floating-deco {
  position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
}
.app {
  min-height: 100vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
.floating-deco .deco {
  position: absolute; font-size: 22px; animation: floatDeco 10s infinite linear; opacity: 0.2;
}
@keyframes floatDeco {
  0% { transform: translateY(100vh) rotate(0deg) scale(0.4); opacity: 0; }
  15% { opacity: 0.2; }
  85% { opacity: 0.15; }
  100% { transform: translateY(-15vh) rotate(720deg) scale(1.1); opacity: 0; }
}
.floating-deco .deco:nth-child(1) { left: 3%; animation-duration: 11s; animation-delay: 0s; font-size: 18px; }
.floating-deco .deco:nth-child(2) { left: 12%; animation-duration: 10s; animation-delay: 2s; font-size: 26px; }
.floating-deco .deco:nth-child(3) { left: 22%; animation-duration: 12s; animation-delay: 4s; font-size: 16px; }
.floating-deco .deco:nth-child(4) { left: 35%; animation-duration: 9s; animation-delay: 1s; font-size: 24px; }
.floating-deco .deco:nth-child(5) { left: 48%; animation-duration: 13s; animation-delay: 3s; font-size: 20px; }
.floating-deco .deco:nth-child(6) { left: 58%; animation-duration: 10s; animation-delay: 5s; font-size: 22px; }
.floating-deco .deco:nth-child(7) { left: 68%; animation-duration: 11s; animation-delay: 2s; font-size: 18px; }
.floating-deco .deco:nth-child(8) { left: 78%; animation-duration: 12s; animation-delay: 0s; font-size: 26px; }
.floating-deco .deco:nth-child(9) { left: 88%; animation-duration: 9s; animation-delay: 4s; font-size: 16px; }
.floating-deco .deco:nth-child(10) { left: 95%; animation-duration: 11s; animation-delay: 3s; font-size: 20px; }

.header {
  background: linear-gradient(135deg, #FFB5C2 0%, #FF8FAB 30%, #D4A5FF 70%, #A8E6CF 100%);
  color: #fff; padding: 28px 20px 36px; text-align: center; position: relative; z-index: 1;
  border-radius: 0 0 36px 36px;
  box-shadow: 0 6px 30px rgba(255,143,171,0.3);
}
.header::after {
  content: '🌸'; position: absolute; top: 8px; right: 16px; font-size: 20px; opacity: 0.5;
}
.header::before {
  content: '✨'; position: absolute; top: 8px; left: 16px; font-size: 20px; opacity: 0.5;
}
.header .greeting { font-size: 14px; opacity: 0.9; margin-bottom: 4px; letter-spacing: 2px; }
.header .name { font-size: 24px; font-weight: 400; margin-bottom: 6px; letter-spacing: 1px; }
.header .name span { display: inline-block; animation: heartBounce 1.2s ease-in-out infinite; }
@keyframes heartBounce {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.2) rotate(-8deg); }
  75% { transform: scale(1.2) rotate(8deg); }
}
.header .clock {
  font-size: 56px; font-weight: 400; letter-spacing: 6px;
  font-variant-numeric: tabular-nums; text-shadow: 0 2px 12px rgba(0,0,0,0.08);
  line-height: 1.1;
}
.header .clock-sep { animation: twinkle 1s step-end infinite; display: inline-block; }
@keyframes twinkle { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
.header .rate-wrap {
  display: inline-flex; align-items: center; gap: 8px; margin-top: 14px;
  background: rgba(255,255,255,0.3); backdrop-filter: blur(8px);
  border-radius: 30px; padding: 6px 20px; font-size: 14px; font-weight: 400;
  border: 1.5px solid rgba(255,255,255,0.3);
}
.header .rate-wrap .num { font-size: 20px; font-weight: 400; }

.container { max-width: 480px; margin: 0 auto; padding: 16px; position: relative; z-index: 1; }

.tip-banner {
  background: linear-gradient(135deg, rgba(255,182,193,0.15), rgba(212,165,255,0.1));
  border-radius: 16px; padding: 14px 18px; margin-bottom: 16px;
  font-size: 14px; color: var(--text); text-align: center; line-height: 1.7;
  border: 1.5px solid rgba(255,182,193,0.12);
}
.tip-banner .tip-icon { font-size: 22px; display: block; margin-bottom: 4px; }

.toolbar {
  position: fixed; bottom: 0; left: 6px; right: 6px;
  background: rgba(255,255,255,0.92); backdrop-filter: blur(16px);
  box-shadow: 0 -2px 24px rgba(255,143,171,0.08);
  display: flex; padding: 6px 8px calc(6px + var(--safe-bottom)); gap: 4px;
  z-index: 20; align-items: center;
  border-radius: 28px 28px 0 0;
  border-top: 1.5px solid rgba(255,182,193,0.12);
}
.toolbar .tab {
  flex: 1; text-align: center; padding: 10px 4px; border: none; background: none;
  font-family: inherit; font-size: 11px; color: var(--text-light); cursor: pointer;
  border-radius: 16px; transition: all 0.2s;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
}
.toolbar .tab .tab-icon { font-size: 24px; transition: all 0.2s; }
.toolbar .tab.active { color: var(--pink); background: rgba(255,143,171,0.08); }
.toolbar .tab.active .tab-icon { animation: tabBounce 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes tabBounce {
  0% { transform: scale(1); } 50% { transform: scale(1.25); } 100% { transform: scale(1.1); }
}
</style>
