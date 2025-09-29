"""
Pydantic schemas for API requests and responses.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ContentCreate(BaseModel):
    topic: str
    style: str | None = None


class ContentOut(BaseModel):
    id: str
    topic: str
    style: str | None
    content: str
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True

