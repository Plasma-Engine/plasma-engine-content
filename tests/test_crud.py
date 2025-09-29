import os
from fastapi.testclient import TestClient

# Use sqlite in-memory for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.main import app  # noqa: E402


client = TestClient(app)


def test_generate_persists_and_fetch_by_id_and_list():
    r = client.post("/api/v1/content/generate", json={"topic": "test db", "style": "dry"})
    assert r.status_code == 200, r.text
    cid = r.json()["id"]

    g = client.get(f"/api/v1/content/{cid}")
    assert g.status_code == 200
    body = g.json()
    assert body["id"] == cid
    assert body["topic"] == "test db"

    lst = client.get("/api/v1/content?limit=10&offset=0")
    assert lst.status_code == 200
    assert isinstance(lst.json(), list)
    assert any(item["id"] == cid for item in lst.json())

