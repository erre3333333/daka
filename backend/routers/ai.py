from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import os
import httpx
import aiosqlite
from database import get_db

router = APIRouter(prefix="/api/ai", tags=["ai"])

def gen_fallback_report(checkins: list, schedules: list) -> str:
    total = len(schedules)
    done = len(checkins)
    rate = round(done / total * 100) if total > 0 else 0
    return f"""## 本周规律性报告

过去 7 天共完成 **{done}** 次打卡，规律率约 **{rate}%**。

### 建议
- 试着固定每天的作息时间
- 睡前 1 小时远离手机
- 每餐定时定量
- 每天保持 30 分钟运动"""

@router.post("/analyze")
async def analyze(range: str = "week", db: aiosqlite.Connection = Depends(get_db)):
    days = 30 if range == "month" else 7
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cursor = await db.execute("SELECT * FROM schedules WHERE enabled=1 ORDER BY hour")
    schedules = [dict(row) for row in await cursor.fetchall()]
    
    cursor = await db.execute("SELECT * FROM checkins WHERE date >= ? AND status='done' ORDER BY date", (start,))
    checkins = [dict(row) for row in await cursor.fetchall()]
    
    api_key = os.environ.get("AGNES_API_KEY")
    if not api_key:
        return {"fallback": gen_fallback_report(checkins, schedules)}
    
    schedule_text = "\n".join([f"- {s['label']}: {str(s['hour']).zfill(2)}:{str(s['minute']).zfill(2)}" for s in schedules])
    checkin_text = "\n".join([f"- {c['date']} {c['slot_id']}: {c['status']}" + (f" ({c['note']})" if c.get('note') else "") for c in checkins])
    
    prompt = f"""你是一个健康生活教练。以下是用过去{range}的作息打卡数据，请用中文给出：

1. **规律性评估**：数据反映出的生活习惯质量
2. **亮点**：做得好的方面
3. **改进建议**：具体可执行的改进方案
4. **下周目标**：2-3 个可量化的目标

作息计划：
{schedule_text}

打卡记录（{len(checkins)} 条）：
{checkin_text}

请用温暖鼓励的语气，给出专业但不严肃的建议。"""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.agnesai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "deepseek-r1", "messages": [{"role": "user", "content": prompt}], "stream": False}
            )
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", gen_fallback_report(checkins, schedules))
            return {"content": content}
    except Exception as e:
        return {"error": str(e), "fallback": "AI 服务暂不可用"}

@router.post("/voice")
async def voice(text: str):
    if not text:
        return {"error": "缺少语音文本"}
    
    api_key = os.environ.get("AGNES_API_KEY")
    if not api_key:
        return {"action": "note", "text": text}
    
    prompt = f"""分析以下语音指令，提取意图和参数。回复格式为 JSON（不要其他文字）。

支持的意图：
1. checkin: 打卡，需提取 slot_id（wake/breakfast/lunch/nap/dinner/exercise/sleep）
2. set_schedule: 修改作息时间，需提取 slot_id 和时间
3. note: 普通记录

示例：
"完成早餐打卡" → {{"action":"checkin","slot_id":"breakfast","status":"done"}}
"把睡觉改成十点半" → {{"action":"set_schedule","slot_id":"sleep","hour":22,"minute":30}}
"今天心情不错" → {{"action":"note","text":"今天心情不错"}}

语音："{text}" """
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.agnesai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "deepseek-r1", "messages": [{"role": "user", "content": prompt}], "stream": False}
            )
            data = response.json()
            raw = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            import json
            try:
                return json.loads(cleaned)
            except:
                return {"action": "note", "text": text}
    except:
        return {"action": "note", "text": text}
