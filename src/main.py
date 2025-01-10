from fastapi import FastAPI

from .users.routers import router as users_router


def get_application() -> FastAPI:
    _app = FastAPI()
    _app.include_router(users_router)
    return _app


app = get_application()
