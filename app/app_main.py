from fastapi import FastAPI

from api.routes import router
from config import settings


def get_app() -> FastAPI:
    app_: FastAPI = FastAPI(
        title=settings.app.name,
        version=settings.app.api_ver,
        docs_url=settings.app.docs_url,
        description=settings.app.description,
    )
    app_.include_router(router)
    return app_


app: FastAPI = get_app()
