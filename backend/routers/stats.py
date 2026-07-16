from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import aiosqlite
from database import get_db

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("")
async def get_stats(range: str = "week", db: aiosqlite.Connection = Depends(get_db)):
    days = 30 if range == "month" else 7
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cursor = await db.execute("""
        SELECT date,
            COUNT(*) as total,
            SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) as done,
            ROUND(CAST(SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100) as rate
        FROM checkins WHERE date >= ? GROUP BY date ORDER BY date
    """, (start,))
    daily = [dict(row) for row in await cursor.fetchall()]
    
    cursor = await db.execute("SELECT COUNT(*) as c FROM checkins WHERE date >= ?", (start,))
    total = (await cursor.fetchone())[0]
    
    cursor = await db.execute("SELECT COUNT(*) as c FROM checkins WHERE date >= ? AND status='done'", (start,))
    done = (await cursor.fetchone())[0]
    
    overall = round(done / total * 100) if total > 0 else 0
    
    return {"daily": daily, "overall": overall, "total": total, "done": done}
