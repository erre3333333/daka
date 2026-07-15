from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScheduleBase(BaseModel):
    id: str
    label: str
    hour: int
    minute: int
    enabled: bool = True

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    label: Optional[str] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    enabled: Optional[bool] = None

class CheckinBase(BaseModel):
    date: str
    slot_id: str
    status: str = "done"
    note: str = ""
    mood: int = 3

class CheckinCreate(CheckinBase):
    pass

class CheckinDelete(BaseModel):
    date: str
    slot_id: str

class StatsResponse(BaseModel):
    daily: list
    overall: int
    total: int
    done: int

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    apparent_temperature: float
    humidity: int
    wind_speed: float
    weather_code: int
    weather_desc: str
    emoji: str

class AIAnalyzeRequest(BaseModel):
    range: str = "week"

class AIAnalyzeResponse(BaseModel):
    content: str
    fallback: Optional[str] = None
