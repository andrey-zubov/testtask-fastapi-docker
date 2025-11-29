import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi import APIRouter

from app.weather import WeatherTaskRunner


router = APIRouter()
task_runner = WeatherTaskRunner()

# todo temp
@router.get("/weather/")
async def get_weather(cities: str):
    if not cities:
        raise HTTPException(status_code=400, detail="City not provided")

    # if data := get_cached_value(city):
    #     return {"message": data}
    [task_runner.create_task(city) for city in cities.split(",")]

    data = await task_runner.execute_tasks()

    return {"message": data}


# todo add configuration
def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
