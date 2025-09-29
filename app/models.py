"""
SQLAlchemy models for the content service.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(String(64), primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    style = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    provider = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

