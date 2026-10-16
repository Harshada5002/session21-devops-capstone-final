/**
 * TaskTable – main data table with actions
 */

import { useState } from 'react';
import { StatusBadge, PriorityBadge } from './Badges';

function formatDate(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function isOverdue(task) {
  if (!task.due_date || task.status === 'DONE') return false;
  return new Date(task.due_date) < new Date();
}

export default function TaskTable({ tasks, loading, onEdit, onDelete }) {
  const [hoveredId, setHoveredId] = useState(null);

  if (loading) {
    return (
      <div className="task-table-wrapper">
        <div className="loading-state">
          <div className="spinner" />
          Loading tasks…
        </div>
      </div>
    );
  }

  if (!tasks.length) {
    return (
      <div className="task-table-wrapper">
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <div className="empty-state-title">No tasks found</div>
          <div className="empty-state-desc">
            Create your first task or adjust the filters above.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="task-table-wrapper">
      <table className="task-table" aria-label="Task list">
        <thead>
          <tr>
            <th style={{ width: '35%' }}>Task</th>
            <th>Assignee</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Due Date</th>
            <th style={{ width: '100px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(task => (
            <tr
              key={task.id}
              onMouseEnter={() => setHoveredId(task.id)}
              onMouseLeave={() => setHoveredId(null)}
              onClick={() => onEdit(task)}
            >
              <td>
                <div className="task-title-cell truncate" style={{ maxWidth: 280 }}>
                  {task.title}
                </div>
                {task.description && (
                  <div className="task-description-cell truncate" style={{ maxWidth: 280 }}>
                    {task.description}
                  </div>
                )}
              </td>
              <td>
                {task.assignee ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-xs)' }}>
                    <div className="user-avatar" style={{ width: 26, height: 26, fontSize: '0.6875rem' }}>
                      {task.assignee.slice(0,2).toUpperCase()}
                    </div>
                    <span style={{ fontSize: '0.875rem' }}>{task.assignee}</span>
                  </div>
                ) : (
                  <span className="text-muted" style={{ fontSize: '0.8125rem' }}>Unassigned</span>
                )}
              </td>
              <td><StatusBadge status={task.status} /></td>
              <td><PriorityBadge priority={task.priority} /></td>
              <td>
                <span style={{
                  fontSize: '0.8125rem',
                  color: isOverdue(task) ? 'var(--color-high)' : 'var(--color-text-secondary)',
                  fontWeight: isOverdue(task) ? 600 : 400,
                }}>
                  {isOverdue(task) && '⚠️ '}
                  {formatDate(task.due_date)}
                </span>
              </td>
              <td onClick={e => e.stopPropagation()}>
                <div className="action-group">
                  <button
                    className="btn btn-ghost btn-sm btn-icon"
                    onClick={() => onEdit(task)}
                    data-tooltip="Edit task"
                    aria-label={`Edit ${task.title}`}
                    id={`edit-task-${task.id}`}
                  >
                    ✏️
                  </button>
                  <button
                    className="btn btn-ghost btn-sm btn-icon"
                    onClick={() => onDelete(task)}
                    data-tooltip="Delete task"
                    aria-label={`Delete ${task.title}`}
                    id={`delete-task-${task.id}`}
                    style={{ color: 'var(--color-high)' }}
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
