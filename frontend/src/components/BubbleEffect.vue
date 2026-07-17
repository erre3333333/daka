<template>
  <canvas ref="canvasRef" class="bubble-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref(null)

const COLORS = [
  'rgba(248,164,184', 'rgba(212,191,255', 'rgba(184,232,208', 'rgba(255,212,184'
]

const SHAPES = [
  'circle', 'heart', 'star', 'diamond', 'hexagon', 'clover', 'double-ring', 'dashed', 'wavy'
]

let animId = null
let bubbles = []
let particles = []
let w = 0
let h = 0
let frameCount = 0

function rand(a, b) { return a + Math.random() * (b - a) }

function createBubble(overrides = {}) {
  const r = rand(20, 50)
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
    shape: SHAPES[Math.floor(Math.random() * SHAPES.length)],
    alive: true,
    respawnTimer: 0
  }
}

function drawShape(ctx, b) {
  const { x, y, r, shape, color, opacity } = b
  const s = `${color},${opacity})`
  const s2 = `${color},${opacity * 0.4})`
  ctx.strokeStyle = s
  ctx.lineWidth = 1.5

  switch (shape) {
    case 'circle':
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke()
      ctx.beginPath(); ctx.arc(x, y, r * 0.85, 0, Math.PI * 2)
      ctx.strokeStyle = s2; ctx.lineWidth = 3; ctx.stroke()
      break

    case 'heart': {
      const s = r * 0.8
      ctx.beginPath()
      ctx.moveTo(x, y + s * 0.3)
      ctx.bezierCurveTo(x, y - s * 0.4, x - s, y - s * 0.3, x - s, y + s * 0.1)
      ctx.bezierCurveTo(x - s, y + s * 0.6, x, y + s, x, y + s)
      ctx.bezierCurveTo(x, y + s, x + s, y + s * 0.6, x + s, y + s * 0.1)
      ctx.bezierCurveTo(x + s, y - s * 0.3, x, y - s * 0.4, x, y + s * 0.3)
      ctx.stroke()
      ctx.strokeStyle = s2; ctx.lineWidth = 3
      ctx.stroke()
      break
    }

    case 'star': {
      ctx.beginPath()
      for (let i = 0; i < 10; i++) {
        const a = (i * Math.PI * 2) / 10 - Math.PI / 2
        const rad = i % 2 === 0 ? r : r * 0.45
        const px = x + Math.cos(a) * rad
        const py = y + Math.sin(a) * rad
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py)
      }
      ctx.closePath(); ctx.stroke()
      break
    }

    case 'diamond': {
      ctx.beginPath()
      ctx.moveTo(x, y - r); ctx.lineTo(x + r, y)
      ctx.lineTo(x, y + r); ctx.lineTo(x - r, y)
      ctx.closePath(); ctx.stroke()
      // inner
      ctx.beginPath()
      ctx.moveTo(x, y - r * 0.7); ctx.lineTo(x + r * 0.7, y)
      ctx.lineTo(x, y + r * 0.7); ctx.lineTo(x - r * 0.7, y)
      ctx.closePath(); ctx.strokeStyle = s2; ctx.lineWidth = 3; ctx.stroke()
      break
    }

    case 'hexagon': {
      ctx.beginPath()
      for (let i = 0; i < 6; i++) {
        const a = (i * Math.PI * 2) / 6 - Math.PI / 6
        const px = x + Math.cos(a) * r
        const py = y + Math.sin(a) * r
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py)
      }
      ctx.closePath(); ctx.stroke()
      break
    }

    case 'clover': {
      ctx.beginPath()
      for (let i = 0; i < 4; i++) {
        const a = (i * Math.PI * 2) / 4
        const cx = x + Math.cos(a) * r * 0.5
        const cy = y + Math.sin(a) * r * 0.5
        ctx.arc(cx, cy, r * 0.55, a - Math.PI * 0.6, a + Math.PI * 0.6)
      }
      ctx.stroke()
      break
    }

    case 'double-ring':
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke()
      ctx.beginPath(); ctx.arc(x, y, r * 0.5, 0, Math.PI * 2)
      ctx.strokeStyle = s2; ctx.lineWidth = 1; ctx.stroke()
      // connecting spokes
      for (let i = 0; i < 6; i++) {
        const a = (i * Math.PI * 2) / 6
        ctx.beginPath()
        ctx.moveTo(x + Math.cos(a) * r * 0.5, y + Math.sin(a) * r * 0.5)
        ctx.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r)
        ctx.strokeStyle = s; ctx.lineWidth = 0.5; ctx.stroke()
      }
      break

    case 'dashed': {
      const segments = 20 + Math.floor(rand(0, 12))
      for (let i = 0; i < segments; i++) {
        const a1 = (i / segments) * Math.PI * 2
        const a2 = ((i + 0.5) / segments) * Math.PI * 2
        ctx.beginPath()
        ctx.arc(x, y, r, a1, a2)
        ctx.strokeStyle = i % 2 === 0 ? s : 'transparent'
        ctx.lineWidth = 1.5
        ctx.stroke()
      }
      break
    }

    case 'wavy': {
      ctx.beginPath()
      const steps = 36
      for (let i = 0; i <= steps; i++) {
        const a = (i / steps) * Math.PI * 2
        const wave = Math.sin(i * 4) * r * 0.08
        const px = x + Math.cos(a) * (r + wave)
        const py = y + Math.sin(a) * (r + wave)
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py)
      }
      ctx.closePath(); ctx.stroke()
      break
    }
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
      // need deeper overlap to pop (0.55 instead of 1.0)
      if (dist < (a.r + b.r) * 0.25) {
        const mx = (a.x + b.x) / 2
        const my = (a.y + b.y) / 2
        spawnParticles(mx, my, a.color)
        spawnParticles(mx, my, b.color)
        a.alive = false
        b.alive = false
        a.respawnTimer = 120
        b.respawnTimer = 150
      }
    }
  }
}

function update() {
  frameCount++
  if (frameCount % 6 === 0) checkCollisions()

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
      b.respawnTimer = rand(40, 100)
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
    drawShape(ctx, b)
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
  bubbles = Array.from({ length: 8 }, () => createBubble())
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
