from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from database import get_db
from models.schemas import ScheduleCreate, ScheduleUpdate

router = APIRouter(prefix="/api/schedules", tags=["schedules"])

@router.get("")
async def get_schedules(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM schedules ORDER BY hour, minute")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

@router.post("")
async def create_schedule(schedule: ScheduleCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM schedules WHERE id=?", (schedule.id,))
    exists = await cursor.fetchone()
    if exists:
        raise HTTPException(status_code=409, detail="id already exists")
    
    await db.execute(
        "INSERT INTO schedules (id, label, hour, minute, enabled) VALUES (?, ?, ?, ?, ?)",
        (schedule.id, schedule.label, schedule.hour, schedule.minute, 1 if schedule.enabled else 0)
    )
    await db.commit()
    return {"ok": True}

@router.put("/{schedule_id}")
async def update_schedule(schedule_id: str, schedule: ScheduleUpdate, db: aiosqlite.Connection = Depends(get_db)):
    updates = []
    params = []
    
    if schedule.label is not None:
        updates.append("label=?")
        params.append(schedule.label)
    if schedule.hour is not None and schedule.minute is not None:
        updates.append("hour=?, minute=?")
        params.extend([schedule.hour, schedule.minute])
    if schedule.enabled is not None:
        updates.append("enabled=?")
        params.append(1 if schedule.enabled else 0)
    
    if not updates:
        raise HTTPException(status_code=400, detail="no fields to update")
    
    params.append(schedule_id)
    await db.execute(f"UPDATE schedules SET {', '.join(updates)} WHERE id=?", params)
    await db.commit()
    return {"ok": True}

@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str, db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM schedules WHERE id=?", (schedule_id,))
    await db.execute("DELETE FROM checkins WHERE slot_id=?", (schedule_id,))
    await db.commit()
    return {"ok": True}
