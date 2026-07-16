from fastapi import APIRouter, Depends
from datetime import datetime
import aiosqlite
from database import get_db
from models.schemas import CheckinCreate, CheckinDelete

router = APIRouter(prefix="/api/checkins", tags=["checkins"])

@router.get("")
async def get_checkins(date: str = None, db: aiosqlite.Connection = Depends(get_db)):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    cursor = await db.execute("SELECT * FROM checkins WHERE date=?", (date,))
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

@router.post("")
async def create_checkin(checkin: CheckinCreate, db: aiosqlite.Connection = Depends(get_db)):
    date = checkin.date or datetime.now().strftime("%Y-%m-%d")
    
    await db.execute("""
        INSERT INTO checkins (date, slot_id, status, note, mood)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(date, slot_id) DO UPDATE SET 
            status=excluded.status, 
            note=excluded.note, 
            mood=excluded.mood
    """, (date, checkin.slot_id, checkin.status, checkin.note, checkin.mood))
    await db.commit()
    return {"ok": True}

@router.delete("")
async def delete_checkin(checkin: CheckinDelete, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute(
        "DELETE FROM checkins WHERE date=? AND slot_id=?", 
        (checkin.date, checkin.slot_id)
    )
    await db.commit()
    return {"ok": True}
