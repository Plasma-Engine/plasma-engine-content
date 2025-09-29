"""
Database session management for the content service.

Uses SQLAlchemy 2.0 style with a simple session dependency.
DATABASE_URL env var is used; falls back to a local SQLite database.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # Default to a local SQLite file for development/testing
    return "sqlite:///./content.db"


DATABASE_URL = _get_database_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    with session_scope() as s:
        yield s

