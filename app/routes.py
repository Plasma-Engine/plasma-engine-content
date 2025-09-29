"""Route registration and API handlers."""

from __future__ import annotations

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from app.settings import get_settings


api = APIRouter(prefix="/api/v1", tags=["api"])


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
    return GenerateResponse(id=content_id, content=text, provider=provider)


def register_routes(app: FastAPI) -> None:
    app.include_router(api)

