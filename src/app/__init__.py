from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import get_settings

__version__ = '0.1.0'

# global app settings
settings = get_settings()


def create_app():
    from .api import router
    from .db import models, init_db

    app = FastAPI(
        title=settings.app_name,
        version=__version__)

    @app.get("/ping")
    async def pong():
        return {"ping": "pong!"}

    @app.on_event("startup")
    def on_startup():
        init_db()

    app.include_router(router, prefix=settings.api_route)
    app.add_middleware(CORSMiddleware, allow_origins=settings.origins)

    return app
