import uvicorn

from fastapi import FastAPI
from fastapi import APIRouter  # todo temp


router = APIRouter()  # todo temp, for init only

# todo temp
@router.get("/weather/")
async def get_weather():
    return {"message": "Hello World"}


# todo add configuration
def create_app():
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", host="127.0.0.1", port=8000)
