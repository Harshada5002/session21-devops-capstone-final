"""
Task CRUD endpoint tests
--------------------------
These are integration tests that exercise the full HTTP → Service → DB
stack using the isolated SQLite test database.

Covers:
- Task creation
- Task retrieval (single and list)
- Task update
- Task deletion
- Search and filtering
- Pagination
- Statistics
- 404 behaviour
- Validation errors (422)
"""

from __future__ import annotations

import pytest


# ── Helpers ───────────────────────────────────────────────────────────────────

def _create_task(client, **kwargs):
    payload = {
        "title": "Test Task",
        "status": "TODO",
        "priority": "MEDIUM",
        **kwargs,
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


# ── Creation ──────────────────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskCreation:
    def test_create_minimal_task(self, client):
        """Only title is required; remaining fields use defaults."""
        response = client.post("/api/tasks", json={"title": "Minimal Task"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["status"] == "TODO"
        assert data["priority"] == "MEDIUM"
        assert data["id"] is not None
        assert data["created_at"] is not None

    def test_create_full_task(self, client):
        payload = {
            "title": "Full Task",
            "description": "A complete task",
            "status": "IN_PROGRESS",
            "priority": "HIGH",
            "assignee": "Alice",
            "due_date": "2030-12-31T00:00:00Z",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Full Task"
        assert data["status"] == "IN_PROGRESS"
        assert data["priority"] == "HIGH"
        assert data["assignee"] == "Alice"

    def test_create_task_missing_title_returns_422(self, client):
        response = client.post("/api/tasks", json={"status": "TODO"})
        assert response.status_code == 422

    def test_create_task_empty_title_returns_422(self, client):
        response = client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_invalid_status_returns_422(self, client):
        response = client.post("/api/tasks", json={"title": "X", "status": "INVALID"})
        assert response.status_code == 422

    def test_create_task_invalid_priority_returns_422(self, client):
        response = client.post("/api/tasks", json={"title": "X", "priority": "ULTRA"})
        assert response.status_code == 422


# ── Retrieval ─────────────────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskRetrieval:
    def test_get_existing_task(self, client):
        created = _create_task(client, title="Get Me")
        response = client.get(f"/api/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Get Me"

    def test_get_nonexistent_task_returns_404(self, client):
        response = client.get("/api/tasks/99999")
        assert response.status_code == 404

    def test_get_invalid_id_returns_422(self, client):
        response = client.get("/api/tasks/not-an-int")
        assert response.status_code == 422

    def test_list_tasks_empty(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_list_tasks_returns_created_tasks(self, client):
        _create_task(client, title="Task A")
        _create_task(client, title="Task B")
        response = client.get("/api/tasks")
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2


# ── Filtering and Search ──────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskFiltering:
    def test_filter_by_status(self, client):
        _create_task(client, title="Todo Task", status="TODO")
        _create_task(client, title="Done Task", status="DONE")
        response = client.get("/api/tasks?status=TODO")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Todo Task"

    def test_filter_by_priority(self, client):
        _create_task(client, title="High Task", priority="HIGH")
        _create_task(client, title="Low Task", priority="LOW")
        response = client.get("/api/tasks?priority=HIGH")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "High Task"

    def test_search_by_title(self, client):
        _create_task(client, title="Fix the login bug")
        _create_task(client, title="Update documentation")
        response = client.get("/api/tasks?search=login")
        data = response.json()
        assert data["total"] == 1
        assert "login" in data["items"][0]["title"].lower()

    def test_search_by_assignee(self, client):
        _create_task(client, title="Task A", assignee="Alice")
        _create_task(client, title="Task B", assignee="Bob")
        response = client.get("/api/tasks?search=Alice")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["assignee"] == "Alice"

    def test_pagination(self, client):
        for i in range(5):
            _create_task(client, title=f"Task {i}")
        response = client.get("/api/tasks?page=1&page_size=2")
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["pages"] == 3

    def test_combined_filter_and_search(self, client):
        _create_task(client, title="Fix bug", status="IN_PROGRESS", priority="HIGH")
        _create_task(client, title="Fix tests", status="TODO", priority="LOW")
        response = client.get("/api/tasks?status=IN_PROGRESS&search=bug")
        data = response.json()
        assert data["total"] == 1


# ── Update ────────────────────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskUpdate:
    def test_update_task_title(self, client):
        task = _create_task(client, title="Old Title")
        response = client.put(f"/api/tasks/{task['id']}", json={"title": "New Title"})
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"

    def test_update_task_status(self, client):
        task = _create_task(client, status="TODO")
        response = client.put(f"/api/tasks/{task['id']}", json={"status": "DONE"})
        assert response.status_code == 200
        assert response.json()["status"] == "DONE"

    def test_partial_update_does_not_clear_other_fields(self, client):
        task = _create_task(client, title="Keep Me", assignee="Alice")
        response = client.put(f"/api/tasks/{task['id']}", json={"status": "DONE"})
        data = response.json()
        assert data["title"] == "Keep Me"
        assert data["assignee"] == "Alice"

    def test_update_nonexistent_task_returns_404(self, client):
        response = client.put("/api/tasks/99999", json={"title": "Ghost"})
        assert response.status_code == 404

    def test_update_with_invalid_status_returns_422(self, client):
        task = _create_task(client, title="T")
        response = client.put(f"/api/tasks/{task['id']}", json={"status": "FLYING"})
        assert response.status_code == 422


# ── Deletion ──────────────────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskDeletion:
    def test_delete_task(self, client):
        task = _create_task(client, title="Delete Me")
        response = client.delete(f"/api/tasks/{task['id']}")
        assert response.status_code == 204

    def test_deleted_task_is_not_found(self, client):
        task = _create_task(client, title="Delete Me")
        client.delete(f"/api/tasks/{task['id']}")
        response = client.get(f"/api/tasks/{task['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete("/api/tasks/99999")
        assert response.status_code == 404


# ── Statistics ────────────────────────────────────────────────────────────────

@pytest.mark.integration
class TestTaskStats:
    def test_stats_with_no_tasks(self, client):
        response = client.get("/api/tasks/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["completion_rate"] == 0.0

    def test_stats_counts_are_accurate(self, client):
        _create_task(client, title="T1", status="TODO")
        _create_task(client, title="T2", status="TODO")
        _create_task(client, title="T3", status="IN_PROGRESS")
        _create_task(client, title="T4", status="DONE")

        response = client.get("/api/tasks/stats")
        data = response.json()
        assert data["total"] == 4
        assert data["todo"] == 2
        assert data["in_progress"] == 1
        assert data["done"] == 1
        assert data["completion_rate"] == 25.0

    def test_stats_high_priority_count(self, client):
        _create_task(client, title="H1", priority="HIGH")
        _create_task(client, title="H2", priority="HIGH")
        _create_task(client, title="L1", priority="LOW")
        response = client.get("/api/tasks/stats")
        data = response.json()
        assert data["high_priority"] == 2
