from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ready_metrics():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}
    r2 = client.get("/ready")
    assert r2.status_code == 200 and r2.json()["status"] in {"ready", "not_ready"}
    r3 = client.get("/metrics")
    assert r3.status_code == 200


def test_generate_content_minimal():
    r = client.post("/api/v1/content/generate", json={"topic": "launch plan", "style": "concise"})
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"id", "content", "provider"}
    assert "launch plan" in body["content"].lower()
