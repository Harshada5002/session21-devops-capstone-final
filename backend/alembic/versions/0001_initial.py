"""Initial schema – create tasks table

Revision ID: 0001_initial
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types first
    task_status_enum = sa.Enum(
        "TODO", "IN_PROGRESS", "DONE", name="task_status_enum"
    )
    task_priority_enum = sa.Enum(
        "LOW", "MEDIUM", "HIGH", name="task_priority_enum"
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            task_status_enum,
            nullable=False,
            server_default="TODO",
        ),
        sa.Column(
            "priority",
            task_priority_enum,
            nullable=False,
            server_default="MEDIUM",
        ),
        sa.Column("assignee", sa.String(length=255), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Indexes
    op.create_index("ix_tasks_id", "tasks", ["id"], unique=False)
    op.create_index("ix_tasks_status", "tasks", ["status"], unique=False)
    op.create_index("ix_tasks_priority", "tasks", ["priority"], unique=False)
    op.create_index("ix_tasks_due_date", "tasks", ["due_date"], unique=False)
    op.create_index(
        "ix_tasks_status_priority", "tasks", ["status", "priority"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_tasks_status_priority", table_name="tasks")
    op.drop_index("ix_tasks_due_date", table_name="tasks")
    op.drop_index("ix_tasks_priority", table_name="tasks")
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")

    # Drop enum types
    sa.Enum(name="task_priority_enum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="task_status_enum").drop(op.get_bind(), checkfirst=True)
