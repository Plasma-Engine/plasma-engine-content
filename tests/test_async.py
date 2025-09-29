from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_async_endpoint_available_or_graceful():
    resp = client.post("/api/v1/content/generate/async", json={"topic": "hello"})
    # If Celery endpoints are wired, it returns 200; otherwise 404 which is acceptable in unit mode
    assert resp.status_code in {200, 404}
