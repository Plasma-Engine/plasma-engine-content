"""Local test configuration for the Content service."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# -- Path management ------------------------------------------------------
# Running pytest in isolation (e.g. inside CI containers) does not guarantee
# that the repository root is present on ``sys.path``. The content service keeps
# its FastAPI application inside ``app/`` so we pre-prend the service root to
# ensure ``import app`` succeeds regardless of the environment bootstrap.
SERVICE_ROOT = Path(__file__).resolve().parent.parent
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.config import ContentSettings
from app.main import create_app


@pytest.fixture
def test_settings():
    """Provide test-specific settings."""
    return ContentSettings(
        app_name="plasma-engine-content-test",
        cors_origins=["http://localhost:3000", "http://localhost:8000"],
        openai_api_key="test-key-123"
    )


@pytest.fixture
def app(test_settings):
    """Create FastAPI app with test settings."""
    return create_app(test_settings)


@pytest.fixture
def client(app):
    """Provide TestClient for the content service."""
    return TestClient(app)


@pytest.fixture
def mock_content_data():
    """Provide mock content data."""
    return {
        "title": "The Future of AI",
        "content": "Artificial Intelligence continues to evolve rapidly...",
        "summary": "An exploration of AI developments",
        "author": "Dr. Jane Smith",
        "tags": ["ai", "technology", "future"],
        "status": "draft",
        "metadata": {
            "word_count": 1500,
            "reading_time": 6,
            "seo_score": 85
        }
    }


@pytest.fixture
def mock_content_list():
    """Provide mock content list."""
    return [
        {
            "id": "content-1",
            "title": "AI Revolution",
            "summary": "The impact of AI on society",
            "status": "published",
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": "content-2",
            "title": "Quantum Computing Guide",
            "summary": "Understanding quantum principles",
            "status": "draft",
            "created_at": "2024-01-16T14:30:00Z"
        }
    ]