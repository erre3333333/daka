import aiosqlite
import os
from pathlib import Path

DB_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
DB_PATH = DB_DIR / "life.db"

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode = WAL")
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL")
        
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS schedules (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                hour INTEGER NOT NULL,
                minute INTEGER NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                slot_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'missed',
                note TEXT DEFAULT '',
                mood INTEGER DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, slot_id)
            );

            CREATE TABLE IF NOT EXISTS ai_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor = await db.execute("SELECT COUNT(*) FROM schedules")
        count = (await cursor.fetchone())[0]
        
        if count == 0:
            defaults = [
                ('wake', '起床', 7, 0),
                ('breakfast', '早餐', 8, 0),
                ('lunch', '午餐', 12, 0),
                ('nap', '午休', 13, 0),
                ('dinner', '晚餐', 18, 0),
                ('exercise', '运动', 20, 0),
                ('sleep', '睡觉', 23, 0),
            ]
            await db.executemany(
                "INSERT INTO schedules (id, label, hour, minute) VALUES (?, ?, ?, ?)",
                defaults
            )
        
        await db.commit()
