"""
Celery worker configuration and tasks for async generation.

Broker and backend are read from environment variables:
  - CELERY_BROKER_URL (default: redis://localhost:6379/0)
  - CELERY_RESULT_BACKEND (default: redis://localhost:6379/1)
"""

from __future__ import annotations

import os
from celery import Celery

from app.routes import _generate_content


broker_url = os.getenv("CELERY_BROKER_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0"))
result_backend = os.getenv("CELERY_RESULT_BACKEND", os.getenv("REDIS_URL", "redis://localhost:6379/1"))

celery_app = Celery(
    "plasma_engine_content",
    broker=broker_url,
    backend=result_backend,
)


@celery_app.task(name="content.generate")
def generate_content_task(topic: str, style: str | None = None) -> dict[str, str]:
    content_id, text = _generate_content(topic, style)
    return {"id": content_id, "content": text}

