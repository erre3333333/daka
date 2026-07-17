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
      <button class="tab" :class="{ active: activeTab === 'weather' }" @click="switchTab('weather')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
        </svg>
        <span>天气</span>
      </button>
      <button class="tab" :class="{ active: activeTab === 'stats' }" @click="switchTab('stats')">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <span>统计</span>
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
  { icon: '☀️', text: '醒来想到你，连空气都是甜的' },
  { icon: '🌸', text: '你比春风更温柔，比阳光更温暖' },
  { icon: '🌟', text: '有你在的世界，每一天都在发光' },
  { icon: '🎀', text: '你认真生活的样子，真的超级迷人' },
  { icon: '💝', text: '爱自己是终身浪漫的开始' },
  { icon: '🦋', text: '你每一次努力，都让未来更闪亮' },
  { icon: '🍯', text: '你是我平淡生活里最甜的糖' },
  { icon: '🌷', text: '你值得世间所有的美好' },
  { icon: '✨', text: '今天也要做闪闪发光的自己哦' },
  { icon: '🌈', text: '不管遇到什么，彩虹总在风雨后' },
  { icon: '🌻', text: '你像向日葵一样，自带阳光' },
  { icon: '💫', text: '你的存在本身就是一种治愈' },
  { icon: '🌺', text: '慢慢来，一切都来得及' },
  { icon: '🍀', text: '今天的你，比昨天更棒了' },
  { icon: '🎵', text: '生活虽然平凡，但有你就不普通' },
  { icon: '🌙', text: '睡前原谅一切，醒来便是新生' },
  { icon: '⭐', text: '你是我眼里最亮的那颗星' },
  { icon: '🌸', text: '每一天都是重新喜欢上你的一天' },
  { icon: '💕', text: '你的笑容是我最大的动力' },
  { icon: '🌊', text: '爱意如潮水，日夜不停歇' },
  { icon: '🍃', text: '微风轻轻吹，我在轻轻想你' },
  { icon: '🌅', text: '每一个日出都让我更期待有你的日子' },
  { icon: '🌄', text: '黄昏再美，也不及你回头一笑' },
  { icon: '🌤', text: '天气很好，心情很好，有你更好' },
  { icon: '☁️', text: '每一朵云都是我想你的形状' },
  { icon: '🌧️', text: '下雨天也想和你窝在一起看剧' },
  { icon: '❄️', text: '冷的时候就想抱抱你' },
  { icon: '🌪️', text: '你像一阵风，把我的世界全都搅乱' },
  { icon: '🌊', text: '对你的喜欢像大海一样深' },
  { icon: '🏔️', text: '翻山越岭只为了见你一面' },
  { icon: '🌲', text: '森林再大也不及我心里的你' },
  { icon: '🦋', text: '你一出现，连蝴蝶都为你跳舞' },
  { icon: '🐚', text: '把想念装进海螺里，你听到了吗' },
  { icon: '🌹', text: '送你一朵玫瑰，代表我的真心' },
  { icon: '💐', text: '所有的花都不及你好看' },
  { icon: '🌻', text: '你是我的小太阳，永远照亮我' },
  { icon: '🌠', text: '流星划过时许的愿都是关于你' },
  { icon: '🎆', text: '和你在一起的每一天都像在放烟花' },
  { icon: '🎇', text: '你是夜空中最亮的那颗星' },
  { icon: '🎈', text: '和你在一起，心情像气球一样飞起来' },
  { icon: '🎉', text: '你的每一次进步都值得盛大庆祝' },
  { icon: '🎊', text: '做你自己，就是最好的庆祝' },
  { icon: '🎁', text: '你是我收到过最好的礼物' },
  { icon: '🧸', text: '想把你抱在怀里，像抱着一只小熊' },
  { icon: '🍭', text: '生活本来就该是甜的' },
  { icon: '🍪', text: '你是生活给我的小饼干' },
  { icon: '🧁', text: '你比蛋糕还甜' },
  { icon: '🍰', text: '和你在一起每天都像过生日' },
  { icon: '🥐', text: '早安，今天也要好好爱自己' },
  { icon: '☕', text: '和你一起喝咖啡，苦也变成甜' },
  { icon: '🍵', text: '温温柔柔地生活，像你一样' },
  { icon: '🥛', text: '每天都要像牛奶一样白白嫩嫩' },
  { icon: '🧃', text: '喝口果汁，给生活加点甜' },
  { icon: '🍇', text: '你是生活里最甜的那颗葡萄' },
  { icon: '🍓', text: '你比草莓还要可爱' },
  { icon: '🍑', text: '你像水蜜桃一样甜到心里' },
  { icon: '🍒', text: '你是我的小樱桃，红红火火' },
  { icon: '🍋', text: '生活有时候酸酸的，但有你就不怕' },
  { icon: '🍊', text: '你是我的阳光橙子' },
  { icon: '🍉', text: '夏天和你一样，清凉又甜蜜' },
  { icon: '🍌', text: '你是我的小香蕉，软软糯糯' },
  { icon: '🍎', text: '一天一个苹果，不如一天一个亲亲' },
  { icon: '🍐', text: '你像梨一样清爽又甜' },
  { icon: '🍍', text: '你是我的小菠萝，酸酸甜甜' },
  { icon: '🥝', text: '你像奇异果一样，外表普通内里超甜' },
  { icon: '🍫', text: '你比巧克力更让人上瘾' },
  { icon: '🍩', text: '你是我的甜甜圈，中间的小洞也被你填满了' },
  { icon: '🧇', text: '想和你一起吃早餐，度过每个清晨' },
  { icon: '🥞', text: '你像松饼一样，温暖又香甜' },
  { icon: '🍦', text: '你是夏天里最甜的那口冰淇淋' },
  { icon: '🎂', text: '你的笑容比蛋糕上的奶油还甜' },
  { icon: '🍿', text: '和你在一起，每一天都像在看电影' },
  { icon: '🌽', text: '你像玉米一样金黄灿烂' },
  { icon: '🥕', text: '多吃蔬菜，像你一样水灵灵' },
  { icon: '🥦', text: '再来点绿色，生活就健康啦' },
  { icon: '🧡', text: '心里满满的都是你' },
  { icon: '💛', text: '你是我的小太阳，金灿灿的' },
  { icon: '💚', text: '绿色代表希望，你代表我的未来' },
  { icon: '💙', text: '你像蓝天一样清澈又广阔' },
  { icon: '💜', text: '你是我的紫霞仙子' },
  { icon: '🤎', text: '你像大地一样温柔又踏实' },
  { icon: '🖤', text: '我的世界里你就是唯一' },
  { icon: '🤍', text: '你像白雪一样纯洁美好' },
  { icon: '💗', text: '心脏扑通扑通，全是因为你' },
  { icon: '💓', text: '每一次心跳都在叫你的名字' },
  { icon: '💖', text: '你是我写不完的浪漫诗篇' },
  { icon: '💘', text: '爱神之箭早就射中了我的心' },
  { icon: '💝', text: '把我的心用缎带包好送给你' },
  { icon: '💟', text: '你是我最温柔的信仰' },
  { icon: '❣️', text: '世界很大，但有你就够了' },
  { icon: '💕', text: '对你的喜欢，比昨天多，比明天少' },
  { icon: '💌', text: '写给你的情书永远写不完' },
  { icon: '💎', text: '你比钻石还珍贵' },
  { icon: '🔮', text: '我预见了未来，未来里全是你' },
  { icon: '🎯', text: '你是我唯一的目标' },
  { icon: '🏆', text: '你是我人生中最大的奖杯' },
  { icon: '🥇', text: '在我心里你永远第一' },
  { icon: '🎼', text: '为你写一首唱不完的歌' },
  { icon: '🎨', text: '你是生活里最绚烂的一笔' },
  { icon: '📖', text: '我们的故事，翻到哪一页都甜' },
  { icon: '🔆', text: '你的存在让一切都明亮起来' },
]

const tabTips = {
  checkin: tips,
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
  font-size: 18px; opacity: 1; color: #5B9B8A; letter-spacing: 1.5px; margin-bottom: 2px;
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
