"""FastAPI bootstrap for the Content automation service."""

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import ContentSettings, get_settings


def create_app(settings: Optional[ContentSettings] = None) -> FastAPI:
    """Return a configured FastAPI application instance."""

    resolved_settings = settings or get_settings()

    app = FastAPI(title=resolved_settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        """Expose health state for orchestrators and integration tests."""

        return {"status": "ok", "service": resolved_settings.app_name}

    return app


app = create_app()

