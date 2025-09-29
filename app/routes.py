"""Route registration and API handlers."""

from __future__ import annotations

from fastapi import APIRouter, FastAPI
from prometheus_client import Counter
from pydantic import BaseModel

from app.settings import get_settings


api = APIRouter(prefix="/api/v1", tags=["api"])

_gen_counter = Counter("content_generations_total", "Total content generations", ["provider"])


class GenerateRequest(BaseModel):
    topic: str
    style: str | None = None


class GenerateResponse(BaseModel):
    id: str
    content: str
    provider: str


def _generate_content(topic: str, style: str | None) -> tuple[str, str]:
    """Stub generation function.

    In a full implementation, this would call model providers based on
    configuration (OpenAI/Anthropic/etc.) and prompt templates.
    """
    settings = get_settings()
    style_text = f" in {style} style" if style else ""
    body = f"An article about {topic}{style_text}."
    # Use a simple deterministic id for demo; replace with UUID in production
    content_id = f"gen-{abs(hash(body)) % 10_000_000}"
    return content_id, body


@api.post("/content/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    content_id, text = _generate_content(req.topic, req.style)
    provider = get_settings().model_provider
    _gen_counter.labels(provider=provider).inc()
    return GenerateResponse(id=content_id, content=text, provider=provider)


# Async generation endpoints (Celery) - only if broker explicitly configured
import os

if os.getenv("CELERY_BROKER_URL") or os.getenv("REDIS_URL"):
    try:
        from app.worker import celery_app, generate_content_task  # type: ignore

        @api.post("/content/generate/async")
        def generate_async(req: GenerateRequest) -> dict[str, str]:
            task = generate_content_task.delay(req.topic, req.style)
            return {"task_id": task.id}

        @api.get("/content/tasks/{task_id}")
        def get_task(task_id: str) -> dict[str, str | dict[str, str] | None]:
            res = celery_app.AsyncResult(task_id)
            payload: dict[str, str | dict[str, str] | None] = {
                "task_id": task_id,
                "state": res.state,
                "result": res.result if res.successful() else None,
            }
            return payload
    except Exception:
        # Celery not configured; endpoints will be absent in this mode.
        pass


def register_routes(app: FastAPI) -> None:
    app.include_router(api)

