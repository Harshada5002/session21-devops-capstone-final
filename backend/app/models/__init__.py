# app/models/__init__.py
# Import all models here so that Alembic can discover them via Base.metadata
from app.models.task import Task, TaskStatus, TaskPriority

__all__ = ["Task", "TaskStatus", "TaskPriority"]
