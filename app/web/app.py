from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.handlers import v1_router
from app.pages.router import router as pages_router
from app.settings.settings import Settings


def create_app() -> FastAPI:
    """Create FastAPI app."""

    settings: Settings = Settings.load()

    app = FastAPI(
        debug=settings.app.debug,
        title=settings.app.title,
        description=settings.app.description
    )

    include_routers(app=app)

    return app


def add_middlewares(app: FastAPI, settings: Settings) -> None:
    """Add middlewares."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.cors_middleware_allow_origins,
        allow_credentials=settings.app.cors_middleware_allow_credentials,
        allow_methods=settings.app.cors_middleware_allow_methods,
        allow_headers=settings.app.cors_middleware_allow_allow_headers
    )


def include_routers(app: FastAPI) -> None:
    """Include routers."""
    app.include_router(v1_router)
    app.include_router(pages_router)
