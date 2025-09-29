"""
Plasma Engine Content service - FastAPI application entrypoint.

Provides baseline operational endpoints and a minimal content generation API.
"""

from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest

from app.routes import register_routes
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
    return app


app = create_app()

