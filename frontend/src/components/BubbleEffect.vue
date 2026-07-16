<template>
  <canvas ref="canvasRef" class="bubble-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref(null)

const COLORS = [
  'rgba(248,164,184', 'rgba(212,191,255', 'rgba(184,232,208', 'rgba(255,212,184'
]

let animId = null
let bubbles = []
let particles = []
let w = 0
let h = 0

function rand(a, b) { return a + Math.random() * (b - a) }

function createBubble(overrides = {}) {
  const r = rand(35, 80)
  return {
    x: overrides.x ?? rand(r, w - r),
    y: overrides.y ?? rand(h * 0.3, h + r),
    r,
    vx: rand(-0.15, 0.15),
    vy: rand(-0.5, -0.15),
    phase: rand(0, Math.PI * 2),
    freq: rand(0.004, 0.012),
    amp: rand(0.2, 0.6),
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
    opacity: rand(0.12, 0.28),
    alive: true,
    respawnTimer: 0
  }
}

function spawnParticles(x, y, color) {
  for (let i = 0; i < 20; i++) {
    const angle = rand(0, Math.PI * 2)
    const speed = rand(1, 4)
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      r: rand(2, 6),
      life: 1,
      decay: rand(0.012, 0.025),
      color
    })
  }
}

function checkCollisions() {
  for (let i = 0; i < bubbles.length; i++) {
    const a = bubbles[i]
    if (!a.alive) continue
    for (let j = i + 1; j < bubbles.length; j++) {
      const b = bubbles[j]
      if (!b.alive) continue
      const dx = a.x - b.x
      const dy = a.y - b.y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < a.r + b.r) {
        const mx = (a.x + b.x) / 2
        const my = (a.y + b.y) / 2
        spawnParticles(mx, my, a.color)
        spawnParticles(mx, my, b.color)
        a.alive = false
        b.alive = false
        a.respawnTimer = 60
        b.respawnTimer = 80
      }
    }
  }
}

function update() {
  checkCollisions()

  for (const b of bubbles) {
    if (!b.alive) {
      if (b.respawnTimer > 0) {
        b.respawnTimer--
      } else {
        Object.assign(b, createBubble())
      }
      continue
    }
    b.phase += b.freq
    b.x += b.vx + Math.sin(b.phase) * b.amp
    b.y += b.vy
    if (b.y + b.r < -20) {
      b.alive = false
      b.respawnTimer = rand(20, 60)
    }
    if (b.x - b.r > w + 20) b.vx = -Math.abs(b.vx)
    if (b.x + b.r < -20) b.vx = Math.abs(b.vx)
  }

  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy
    p.vy += 0.02
    p.life -= p.decay
  }
  particles = particles.filter(p => p.life > 0)
}

function draw(ctx) {
  ctx.clearRect(0, 0, w, h)

  for (const b of bubbles) {
    if (!b.alive) continue
    ctx.beginPath()
    ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2)
    ctx.strokeStyle = `${b.color},${b.opacity})`
    ctx.lineWidth = 1.5
    ctx.stroke()
    // inner glow
    ctx.beginPath()
    ctx.arc(b.x, b.y, b.r * 0.85, 0, Math.PI * 2)
    ctx.strokeStyle = `${b.color},${b.opacity * 0.4})`
    ctx.lineWidth = 3
    ctx.stroke()
  }

  for (const p of particles) {
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r * p.life, 0, Math.PI * 2)
    ctx.fillStyle = `${p.color},${p.life * 0.7})`
    ctx.fill()
  }
}

function loop(ctx) {
  update()
  draw(ctx)
  animId = requestAnimationFrame(() => loop(ctx))
}

function resize() {
  const canvas = canvasRef.value
  if (!canvas) return
  w = canvas.parentElement.clientWidth
  h = canvas.parentElement.clientHeight
  canvas.width = w
  canvas.height = h
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  resize()
  window.addEventListener('resize', resize)
  bubbles = Array.from({ length: 10 }, () => createBubble())
  loop(ctx)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  window.removeEventListener('resize', resize)
})
</script>

<style scoped>
.bubble-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}
</style>
