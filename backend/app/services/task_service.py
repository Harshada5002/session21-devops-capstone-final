"""
Task Service Layer
------------------
Pure database logic – no HTTP concerns here.
Routers call these functions and translate the return values
into HTTP responses.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskStats, TaskUpdate


# ── Read ──────────────────────────────────────────────────────────────────────

def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.get(Task, task_id)


def list_tasks(
    db: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    """Return a paginated, filtered task list."""
    stmt = select(Task)

    if status:
        stmt = stmt.where(Task.status == status)
    if priority:
        stmt = stmt.where(Task.priority == priority)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Task.title.ilike(pattern),
                Task.description.ilike(pattern),
                Task.assignee.ilike(pattern),
            )
        )

    # Count total before pagination
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total: int = db.execute(count_stmt).scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    stmt = stmt.order_by(Task.created_at.desc()).offset(offset).limit(page_size)
    items = db.execute(stmt).scalars().all()

    pages = max(1, math.ceil(total / page_size))
    return items, total, pages


# ── Write ─────────────────────────────────────────────────────────────────────

def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, payload: TaskUpdate) -> Task:
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(task, field, value)
    # Manually set updated_at because SQLAlchemy onupdate fires only on
    # explicit UPDATE statements – refresh it here for test predictability.
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


# ── Statistics ────────────────────────────────────────────────────────────────

def get_stats(db: Session) -> TaskStats:
    now = datetime.now(timezone.utc)

    total: int = db.execute(select(func.count(Task.id))).scalar_one()
    todo: int = db.execute(
        select(func.count(Task.id)).where(Task.status == TaskStatus.TODO)
    ).scalar_one()
    in_progress: int = db.execute(
        select(func.count(Task.id)).where(Task.status == TaskStatus.IN_PROGRESS)
    ).scalar_one()
    done: int = db.execute(
        select(func.count(Task.id)).where(Task.status == TaskStatus.DONE)
    ).scalar_one()
    overdue: int = db.execute(
        select(func.count(Task.id)).where(
            Task.due_date < now,
            Task.status != TaskStatus.DONE,
        )
    ).scalar_one()
    high_priority: int = db.execute(
        select(func.count(Task.id)).where(Task.priority == TaskPriority.HIGH)
    ).scalar_one()

    completion_rate = round(done / total * 100, 1) if total > 0 else 0.0

    return TaskStats(
        total=total,
        todo=todo,
        in_progress=in_progress,
        done=done,
        overdue=overdue,
        high_priority=high_priority,
        completion_rate=completion_rate,
    )
