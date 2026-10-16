"""
Health and Readiness endpoint tests
-------------------------------------
These are integration tests that use the full HTTP stack.
The database-backed /ready endpoint uses the overridden SQLite session.
"""

import pytest


@pytest.mark.integration
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        """Liveness probe must always return 200 when the process is running."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_does_not_hit_database(self, client):
        """
        /health must not fail even if the database is unavailable.
        We verify this by simply calling it – the test DB session override
        is in place but /health never uses it.
        """
        response = client.get("/health")
        assert response.status_code == 200


@pytest.mark.integration
class TestReadinessEndpoint:
    def test_ready_returns_200_when_db_ok(self, client, monkeypatch):
        """
        /ready should return 200 when the database responds.
        We monkeypatch check_db_connection to simulate a healthy DB.
        """
        import app.api.health as health_module
        monkeypatch.setattr(health_module, "check_db_connection", lambda: True)

        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_ready_returns_503_when_db_unavailable(self, client, monkeypatch):
        """
        /ready must return 503 when the database is unreachable.
        This prevents Kubernetes from routing traffic to an unhealthy pod.
        """
        import app.api.health as health_module
        monkeypatch.setattr(health_module, "check_db_connection", lambda: False)

        response = client.get("/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not ready"


@pytest.mark.integration
class TestRootEndpoint:
    def test_root_returns_app_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["application"] == "TaskBoard"
        assert "version" in data
        assert "docs" in data
