import express from 'express'
import cors from 'cors'
import initSqlJs from 'sql.js'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const app = express()
const PORT = process.env.PORT || 8080
const DATA_DIR = process.env.DATA_DIR || join(__dirname, 'data')
const PUBLIC_DIR = join(__dirname, 'public')
const DB_PATH = join(DATA_DIR, 'life.db')

if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true })

const SQL = await initSqlJs()
let db
if (existsSync(DB_PATH)) {
  db = new SQL.Database(readFileSync(DB_PATH))
} else {
  db = new SQL.Database()
}

function saveDb() { writeFileSync(DB_PATH, Buffer.from(db.export())) }

db.run(`CREATE TABLE IF NOT EXISTS schedules (
  id TEXT PRIMARY KEY, label TEXT NOT NULL, hour INTEGER NOT NULL,
  minute INTEGER NOT NULL, enabled INTEGER NOT NULL DEFAULT 1
)`)
db.run(`CREATE TABLE IF NOT EXISTS checkins (
  id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, slot_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'missed', note TEXT DEFAULT '', mood INTEGER DEFAULT 3,
  created_at TEXT DEFAULT (datetime('now','localtime')), UNIQUE(date, slot_id)
)`)
saveDb()

function queryAll(sql, params = []) {
  const stmt = db.prepare(sql); if (params.length) stmt.bind(params)
  const rows = []; while (stmt.step()) rows.push(stmt.getAsObject()); stmt.free(); return rows
}
function queryOne(sql, params = []) {
  const stmt = db.prepare(sql); if (params.length) stmt.bind(params)
  let row = null; if (stmt.step()) row = stmt.getAsObject(); stmt.free(); return row
}
function run(sql, params = []) { db.run(sql, params); saveDb() }

const count = queryOne('SELECT COUNT(*) as c FROM schedules')
if (count.c === 0) {
  for (const d of [['wake','起床',7,0],['breakfast','早餐',8,0],['lunch','午餐',12,0],['nap','午休',13,0],['dinner','晚餐',18,0],['exercise','运动',20,0],['sleep','睡觉',23,0]])
    run('INSERT INTO schedules (id,label,hour,minute) VALUES (?,?,?,?)', d)
}

app.use(cors()); app.use(express.json())
if (existsSync(PUBLIC_DIR)) app.use('/assets', express.static(join(PUBLIC_DIR, 'assets')))

app.get('/api/health', (req, res) => res.json({ status: 'ok', version: '3.0.0' }))

// Schedules
app.get('/api/schedules', (req, res) => res.json(queryAll('SELECT * FROM schedules ORDER BY hour,minute')))
app.post('/api/schedules', (req, res) => {
  const { id, label, hour, minute, enabled } = req.body
  if (!id || !label) return res.status(400).json({ error: 'missing id or label' })
  if (queryOne('SELECT id FROM schedules WHERE id=?', [id])) return res.status(409).json({ error: 'exists' })
  run('INSERT INTO schedules (id,label,hour,minute,enabled) VALUES (?,?,?,?,?)', [id, label, hour||8, minute||0, enabled!==false?1:0])
  res.json({ ok: true })
})
app.put('/api/schedules/:id', (req, res) => {
  const { id } = req.params; const { label, hour, minute, enabled } = req.body
  const u = [], p = []
  if (label !== undefined) { u.push('label=?'); p.push(label) }
  if (hour !== undefined && minute !== undefined) { u.push('hour=?,minute=?'); p.push(hour, minute) }
  if (enabled !== undefined) { u.push('enabled=?'); p.push(enabled?1:0) }
  if (!u.length) return res.status(400).json({ error: 'no fields' })
  p.push(id); run(`UPDATE schedules SET ${u.join(',')} WHERE id=?`, p); res.json({ ok: true })
})
app.delete('/api/schedules/:id', (req, res) => {
  run('DELETE FROM schedules WHERE id=?', [req.params.id]); run('DELETE FROM checkins WHERE slot_id=?', [req.params.id]); res.json({ ok: true })
})

// Checkins
app.get('/api/checkins', (req, res) => res.json(queryAll('SELECT * FROM checkins WHERE date=?', [req.query.date || new Date().toISOString().slice(0,10)])))
app.post('/api/checkins', (req, res) => {
  const { date, slot_id, status, note, mood } = req.body; const d = date || new Date().toISOString().slice(0,10)
  run(`INSERT INTO checkins (date,slot_id,status,note,mood) VALUES (?,?,?,?,?) ON CONFLICT(date,slot_id) DO UPDATE SET status=excluded.status,note=excluded.note,mood=excluded.mood`,
    [d, slot_id, status||'done', note||'', mood||3]); res.json({ ok: true })
})
app.delete('/api/checkins', (req, res) => {
  const { date, slot_id } = req.body; run('DELETE FROM checkins WHERE date=? AND slot_id=?', [date||new Date().toISOString().slice(0,10), slot_id]); res.json({ ok: true })
})

// Stats
app.get('/api/stats', (req, res) => {
  const range = req.query.range || 'week'; const days = range==='month'?30:7
  const start = new Date(Date.now()-days*86400000).toISOString().slice(0,10)
  const schedules = queryAll("SELECT id FROM schedules WHERE enabled=1")
  const totalSlots = schedules.length || 1
  const daily = queryAll(`SELECT date,COUNT(*) as total,SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) as done,ROUND(CAST(SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) AS REAL)/?*100) as rate FROM checkins WHERE date>=? GROUP BY date ORDER BY date`, [totalSlots, start])
  const done = queryOne("SELECT COUNT(*) as c FROM checkins WHERE date>=? AND status='done'", [start])
  res.json({ daily, overall: Math.round(done.c/totalSlots*100), total: totalSlots, done: done.c })
})

// Weather
const COORDS = { harbin:{lat:45.75,lon:126.65,name:'哈尔滨'}, xian:{lat:34.26,lon:108.94,name:'西安'} }
const WMO={0:'晴',1:'大部晴',2:'多云',3:'阴',45:'雾',48:'雾凇',51:'小毛毛雨',53:'毛毛雨',55:'大毛毛雨',61:'小雨',63:'中雨',65:'大雨',66:'冻雨',67:'大冻雨',71:'小雪',73:'中雪',75:'大雪',77:'雪粒',80:'小阵雨',81:'阵雨',82:'大阵雨',83:'小阵雪',84:'大阵雪',95:'雷暴',96:'雷暴+小冰雹',99:'雷暴+大冰雹'}
const WMO_E={0:'☀️',1:'🌤',2:'⛅',3:'☁️',45:'🌫',48:'🌫',51:'🌦',53:'🌦',55:'🌧',61:'🌧',63:'🌧',65:'🌧',66:'🌧',67:'🌧',71:'🌨',73:'🌨',75:'❄️',77:'🌨',80:'🌦',81:'🌧',82:'🌧',83:'🌨',84:'🌨',95:'⛈',96:'⛈',99:'⛈'}

app.get('/api/weather', async (req, res) => {
  const c = COORDS[req.query.city]; if (!c) return res.status(400).json({ error: 'invalid city' })
  try {
    const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${c.lat}&longitude=${c.lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,visibility&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Asia/Shanghai`, { signal: AbortSignal.timeout(8000) })
    const data = await r.json(); const cur = data.current||{}; const daily = data.daily||{}; const code = cur.weather_code||0
    res.json({ city:c.name, temperature:cur.temperature_2m||0, apparent_temperature:cur.apparent_temperature||0, humidity:cur.relative_humidity_2m||0, wind_speed:cur.wind_speed_10m||0, weather_code:code, weather_desc:WMO[code]||'未知', emoji:WMO_E[code]||'❓', temp_max:(daily.temperature_2m_max||[0])[0], temp_min:(daily.temperature_2m_min||[0])[0] })
  } catch(e) { res.status(502).json({ error: e.message }) }
})

// AI
app.post('/api/ai/analyze', (req, res) => {
  const range = req.query.range||'week'; const days = range==='month'?30:7
  const start = new Date(Date.now()-days*86400000).toISOString().slice(0,10)
  const schedules = queryAll("SELECT * FROM schedules WHERE enabled=1 ORDER BY hour")
  const done = queryOne("SELECT COUNT(*) as c FROM checkins WHERE date>=? AND status='done'", [start])
  const rate = schedules.length>0?Math.round(done.c/schedules.length*100):0
  res.json({ content: `## 本周规律性报告\n\n过去 ${days} 天共完成 **${done.c}** 次打卡，规律率约 **${rate}%**。\n\n### 建议\n- 试着固定每天的作息时间\n- 睡前 1 小时远离手机\n- 每餐定时定量\n- 每天保持 30 分钟运动` })
})

// Static files
if (existsSync(PUBLIC_DIR)) {
  app.use(express.static(PUBLIC_DIR))
}

// SPA Fallback
if (existsSync(PUBLIC_DIR)) {
  app.get('*', (req, res) => { if (!req.path.startsWith('/api')) res.sendFile(join(PUBLIC_DIR, 'index.html')) })
}

app.listen(PORT, () => console.log(`🌸 宝宝生活小助手 v3 已启动: http://localhost:${PORT}`))
