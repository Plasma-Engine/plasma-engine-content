"""Configuration handling for the Content automation service."""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class ContentSettings(BaseSettings):
    """Settings container for content generation service."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application Settings
    app_name: str = "plasma-engine-content"
    environment: str = "development"
    debug: bool = False
    port: int = 8002
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # AI API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Database Settings
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # Content Generation Settings
    default_model: str = "gpt-4o-mini"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # Template Settings
    templates_dir: str = "templates"
    
    # Rate Limiting
    requests_per_minute: int = 60
    
    # Content Limits
    max_content_length: int = 10000
    max_batch_size: int = 10


@lru_cache
def get_settings() -> ContentSettings:
    """Factory providing cached settings instance."""

    return ContentSettings()

