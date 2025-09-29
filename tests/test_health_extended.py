import pytest
from app.main import create_app

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    app = create_app()
    return TestClient(app)

def test_health_endpoint(client):
    """Test health check endpoint returns OK."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_readiness_endpoint(client):
    """Test readiness check endpoint with LangChain status."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["langchain_available"] is True
    assert data["ai_generation_ready"] is True

def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "features" in data
    assert "ai_generation" in data["features"]
    assert "brand_voice" in data["features"]
    assert "content_calendar" in data["features"]
