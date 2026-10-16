"""
Pydantic Schemas – Task
------------------------
Defines request and response shapes for the Task resource.
These schemas are separate from the ORM model to keep serialisation
concerns out of the persistence layer.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TaskPriority, TaskStatus


# ── Shared base ───────────────────────────────────────────────────────────────
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["Design homepage"])
    description: Optional[str] = Field(None, max_length=4096)
    status: TaskStatus = Field(TaskStatus.TODO)
    priority: TaskPriority = Field(TaskPriority.MEDIUM)
    assignee: Optional[str] = Field(None, max_length=255, examples=["Alice"])
    due_date: Optional[datetime] = Field(None)


# ── Create request ────────────────────────────────────────────────────────────
class TaskCreate(TaskBase):
    pass


# ── Update request (all fields optional for partial updates) ──────────────────
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=4096)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = Field(None, max_length=255)
    due_date: Optional[datetime] = None


# ── Database / response schema ────────────────────────────────────────────────
class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ── Paginated list response ───────────────────────────────────────────────────
class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int


# ── Statistics response ───────────────────────────────────────────────────────
class TaskStats(BaseModel):
    total: int
    todo: int
    in_progress: int
    done: int
    overdue: int
    high_priority: int
    completion_rate: float  # 0.0 – 100.0
