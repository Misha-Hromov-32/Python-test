from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .core.config import ensure_directories, get_settings
from .database import init_db, ensure_default_users
from .routers import auth, movies


def create_app() -> FastAPI:
    settings = get_settings()
    ensure_directories(settings)

    app = FastAPI(
        title=settings.app_name,
        description=settings.description,
    )

    app.include_router(auth.router, tags=["auth"])
    app.include_router(movies.router, tags=["movies"])

    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()
        ensure_default_users()

    return app

