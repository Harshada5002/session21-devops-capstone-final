"""
Tasks Router
------------
All task-related HTTP endpoints.

Design decisions:
- /api/tasks/stats MUST be registered before /api/tasks/{id}
  so FastAPI doesn't interpret "stats" as an integer id.
- Validation errors automatically return 422 via FastAPI / Pydantic.
- Service layer handles all DB logic; this router only translates
  between HTTP and Python objects.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import (
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskStats,
    TaskUpdate,
)
from app.services import task_service

router = APIRouter()


# ── Statistics (must come before /{id}) ──────────────────────────────────────
@router.get(
    "/tasks/stats",
    response_model=TaskStats,
    summary="Dashboard statistics",
)
def get_stats(db: Session = Depends(get_db)):
    """Return aggregate counts for the KPI cards on the dashboard."""
    return task_service.get_stats(db)


# ── List tasks ────────────────────────────────────────────────────────────────
@router.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="List tasks",
)
def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, min_length=1, description="Full-text search"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    items, total, pages = task_service.list_tasks(
        db, status=status, priority=priority, search=search,
        page=page, page_size=page_size,
    )
    return TaskListResponse(
        items=items, total=total, page=page, page_size=page_size, pages=pages
    )


# ── Get single task ───────────────────────────────────────────────────────────
@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return task


# ── Create task ───────────────────────────────────────────────────────────────
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, payload)


# ── Update task ───────────────────────────────────────────────────────────────
@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return task_service.update_task(db, task, payload)


# ── Delete task ───────────────────────────────────────────────────────────────
@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    task_service.delete_task(db, task)
