from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/weather", tags=["weather"])

WEATHER_COORDS = {
    "harbin": {"lat": 45.75, "lon": 126.65, "name": "哈尔滨"},
    "xian": {"lat": 34.26, "lon": 108.94, "name": "西安"},
}

WMO_CODE = {
    0: "晴", 1: "大部晴", 2: "多云", 3: "阴",
    45: "雾", 48: "雾凇",
    51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨", 66: "冻雨", 67: "大冻雨",
    71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒",
    80: "小阵雨", 81: "阵雨", 82: "大阵雨", 83: "小阵雪", 84: "大阵雪",
    95: "雷暴", 96: "雷暴+小冰雹", 99: "雷暴+大冰雹",
}

WMO_EMOJI = {
    0: "☀️", 1: "🌤", 2: "⛅", 3: "☁️",
    45: "🌫", 48: "🌫",
    51: "🌦", 53: "🌦", 55: "🌧",
    61: "🌧", 63: "🌧", 65: "🌧", 66: "🌧", 67: "🌧",
    71: "🌨", 73: "🌨", 75: "❄️", 77: "🌨",
    80: "🌦", 81: "🌧", 82: "🌧", 83: "🌨", 84: "🌨",
    95: "⛈", 96: "⛈", 99: "⛈",
}

@router.get("")
async def get_weather(city: str):
    if city not in WEATHER_COORDS:
        raise HTTPException(status_code=400, detail="invalid city")
    
    coords = WEATHER_COORDS[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,visibility&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Asia/Shanghai"
    
    async with httpx.AsyncClient(timeout=8.0) as client:
        try:
            response = await client.get(url)
            data = response.json()
            
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            weather_code = current.get("weather_code", 0)
            
            return {
                "city": coords["name"],
                "temperature": current.get("temperature_2m", 0),
                "apparent_temperature": current.get("apparent_temperature", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "wind_speed": current.get("wind_speed_10m", 0),
                "weather_code": weather_code,
                "weather_desc": WMO_CODE.get(weather_code, "未知"),
                "emoji": WMO_EMOJI.get(weather_code, "❓"),
                "temp_max": daily.get("temperature_2m_max", [0])[0],
                "temp_min": daily.get("temperature_2m_min", [0])[0],
            }
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
