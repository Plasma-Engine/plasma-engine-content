"""Smoke tests for the Content service health endpoint."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_content_status() -> None:
    """Ensure /health responds with the correct service identifier."""

    client = TestClient(create_app())
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "plasma-engine-content"

