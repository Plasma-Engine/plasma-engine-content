"""Configuration handling for the Content automation service."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class ContentSettings(BaseSettings):
    """Settings container with inline documentation for hand-off clarity."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "plasma-engine-content"
    cors_origins: List[str] = ["http://localhost:3000"]
    openai_api_key: str | None = None


@lru_cache
def get_settings() -> ContentSettings:
    """Factory providing cached settings instance."""

    return ContentSettings()

