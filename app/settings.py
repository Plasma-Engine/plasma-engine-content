"""Environment-driven settings for the content service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str
    version: str
    debug: bool
    model_provider: str
    openai_api_key: str | None
    anthropic_api_key: str | None


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_settings() -> Settings:
    env = os.getenv("APP_ENV", "development")
    return Settings(
        environment=env,
        version=os.getenv("APP_VERSION", "0.1.0"),
        debug=_bool(os.getenv("APP_DEBUG"), default=(env != "production")),
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

