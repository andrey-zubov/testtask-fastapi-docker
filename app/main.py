import uvicorn
import traceback

from fastapi import FastAPI, HTTPException
from fastapi import APIRouter

from app.weather import WeatherTaskRunner
from app.weathercache import WeatherCache  # импортируем наш синглтон Cache

router = APIRouter()

@router.get("/weather/")
async def get_weather(cities: str):
    if not cities:
        raise HTTPException(status_code=400, detail="City not provided")

    task_runner = WeatherTaskRunner(WeatherCache())

    [task_runner.create_task(city) for city in cities.split(",")]

    try:
        data = await task_runner.execute_tasks()
    except Exception as e:
        traceback.print_exc(e)
        return traceback.format_exc(e)

    return data


# todo add configuration
def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
