import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi import APIRouter

from app.weather import WeatherTaskRunner


router = APIRouter()

@router.get("/weather/")
async def get_weather(cities: str):
    if not cities:
        raise HTTPException(status_code=400, detail="City not provided")

    task_runner = WeatherTaskRunner()

    # if data := get_cached_value(city):
    #     return {"message": data}
    [task_runner.create_task(city) for city in cities.split(",")]

    try:
        data = await task_runner.execute_tasks()
    except Exception as e:
        print(e)  # todo traceback it and log
        return str(e)

    return data


# todo add configuration
def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
