"""
Plasma Engine Content service - FastAPI application entrypoint.

Provides baseline operational endpoints and a minimal content generation API.
"""

from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest

from sqlalchemy import inspect

from app.routes import register_routes
from app.db import engine
from app.models import Base
from app.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Plasma Engine Content",
        version=settings.version,
        description="AI-powered content generation and publishing service.",
    )

    # Minimal in-process metrics
    registry = CollectorRegistry()
    liveness_gauge = Gauge("content_liveness", "Liveness state", registry=registry)
    readiness_gauge = Gauge("content_readiness", "Readiness state", registry=registry)
    liveness_gauge.set(1)
    readiness_gauge.set(1)

    @app.get("/health", tags=["ops"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", tags=["ops"])
    def ready() -> dict[str, str]:
        try:
            _ = get_settings()
            readiness_gauge.set(1)
            return {"status": "ready"}
        except Exception:
            readiness_gauge.set(0)
            return {"status": "not_ready"}

    @app.get("/metrics", tags=["ops"])
    def metrics() -> Response:
        data = generate_latest(registry)
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    register_routes(app)
    # Ensure tables exist (basic bootstrap for dev/test). In production, use migrations.
    try:
        inspector = inspect(engine)
        if not inspector.has_table("content_items"):
            Base.metadata.create_all(bind=engine)
    except Exception:
        # Do not fail the app if DB is unavailable during startup.
        pass
    return app


app = create_app()

