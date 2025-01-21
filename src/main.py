from fastapi import FastAPI

from .users.routers import router as users_router
from .auth.routers import router as auth_router


def get_application() -> FastAPI:
    _app = FastAPI()
    _app.include_router(users_router)
    _app.include_router(auth_router)
    return _app


app = get_application()
