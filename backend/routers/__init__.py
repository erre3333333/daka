from fastapi import APIRouter
from . import schedules, checkins, stats, weather, ai

router = APIRouter()
router.include_router(schedules.router)
router.include_router(checkins.router)
router.include_router(stats.router)
router.include_router(weather.router)
router.include_router(ai.router)
