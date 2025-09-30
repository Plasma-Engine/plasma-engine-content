"""Tests for the Content service main application."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app
from app.config import ContentSettings


class TestContentApp:
    """Test the Content service FastAPI application."""

    def test_creates_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance."""
        app = create_app()
        assert isinstance(app, FastAPI)

    def test_health_endpoint_returns_correct_service_name(self, client, test_settings):
        """Test health endpoint returns content service name."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == test_settings.app_name

    def test_cors_middleware_configuration(self, test_settings):
        """Test CORS middleware allows configured origins."""
        app = create_app(test_settings)
        client = TestClient(app)

        response = client.get("/health", headers={
            "Origin": "http://localhost:3000"
        })

        assert response.status_code == 200

    def test_app_handles_404_correctly(self, client):
        """Test that non-existent endpoints return 404."""
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404

    def test_health_endpoint_performance(self, client):
        """Test health endpoint responds quickly."""
        import time

        start_time = time.perf_counter()
        response = client.get("/health")
        end_time = time.perf_counter()

        assert response.status_code == 200
        assert (end_time - start_time) < 0.1  # Less than 100ms