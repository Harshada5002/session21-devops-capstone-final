/**
 * Dashboard page
 * ---------------
 * The main application view.  Assembles all components and wires
 * up the useTasks hook.
 */

import { useState } from 'react';
import { useTasks } from '../hooks/useTasks';
import KpiCards from '../components/KpiCards';
import TaskTable from '../components/TaskTable';
import TaskModal from '../components/TaskModal';
import ConfirmDialog from '../components/ConfirmDialog';
import Pipeline from '../components/Pipeline';
import ActivityFeed from '../components/ActivityFeed';

const STATUS_FILTERS = [
  { label: 'All',         value: '' },
  { label: '📋 To Do',    value: 'TODO' },
  { label: '🔄 In Progress', value: 'IN_PROGRESS' },
  { label: '✅ Done',     value: 'DONE' },
];

const PRIORITY_FILTERS = [
  { label: 'Any Priority', value: '' },
  { label: '↑ High',  value: 'HIGH' },
  { label: '— Medium',value: 'MEDIUM' },
  { label: '↓ Low',   value: 'LOW' },
];

export default function Dashboard() {
  const {
    tasks, stats, loading, error,
    filters, pagination,
    applyFilter, setPage,
    addTask, editTask, removeTask,
  } = useTasks();

  const [showModal, setShowModal]     = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [deletingTask, setDeletingTask] = useState(null);
  const [isDeleting, setIsDeleting]   = useState(false);

  const openCreate = () => { setEditingTask(null); setShowModal(true); };
  const openEdit   = (task) => { setEditingTask(task); setShowModal(true); };
  const closeModal = () => { setShowModal(false); setEditingTask(null); };

  const handleSave = async (payload) => {
    if (editingTask) {
      await editTask(editingTask.id, payload);
    } else {
      await addTask(payload);
    }
  };

  const handleDeleteConfirm = async (id) => {
    setIsDeleting(true);
    try {
      await removeTask(id);
      setDeletingTask(null);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <main className="content">
      <h1 style={{ marginBottom: 'var(--space-xl)', background: 'linear-gradient(135deg, #e8eaf6, #6366f1)', WebkitBackgroundClip: 'text', backgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
        Project Dashboard
      </h1>

      {/* Error banner */}
      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {/* KPI Cards */}
      <KpiCards stats={stats} loading={loading} />

      {/* Pipeline */}
      {stats && <Pipeline stats={stats} />}

      {/* Task section header */}
      <div className="section-header" style={{ marginBottom: 'var(--space-sm)' }}>
        <h2 className="section-title">
          Tasks
          {pagination.total > 0 && (
            <span style={{ fontSize: '0.875rem', fontWeight: 400, color: 'var(--color-text-muted)', marginLeft: 8 }}>
              ({pagination.total})
            </span>
          )}
        </h2>
        <button id="create-task-btn" className="btn btn-primary" onClick={openCreate}>
          ＋ Create Task
        </button>
      </div>

      {/* Filters */}
      <div className="filter-bar" style={{ marginBottom: 'var(--space-md)' }}>
        {STATUS_FILTERS.map(f => (
          <button
            key={f.value}
            className={`filter-chip ${filters.status === f.value ? 'active' : ''}`}
            onClick={() => applyFilter('status', f.value)}
            id={`filter-status-${f.value || 'all'}`}
          >
            {f.label}
          </button>
        ))}
        <div style={{ height: 24, width: 1, background: 'var(--color-border)', margin: '0 4px' }} />
        {PRIORITY_FILTERS.map(f => (
          <button
            key={f.value}
            className={`filter-chip ${filters.priority === f.value ? 'active' : ''}`}
            onClick={() => applyFilter('priority', f.value)}
            id={`filter-priority-${f.value || 'all'}`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Task table */}
      <TaskTable
        tasks={tasks}
        loading={loading}
        onEdit={openEdit}
        onDelete={setDeletingTask}
      />

      {/* Pagination */}
      {pagination.pages > 1 && (
        <div className="pagination">
          <span className="pagination-info">
            Page {pagination.page} of {pagination.pages} · {pagination.total} tasks
          </span>
          <div className="pagination-controls">
            <button
              className="btn btn-secondary btn-sm"
              disabled={pagination.page <= 1}
              onClick={() => setPage(pagination.page - 1)}
              id="pagination-prev"
            >
              ← Prev
            </button>
            <button
              className="btn btn-secondary btn-sm"
              disabled={pagination.page >= pagination.pages}
              onClick={() => setPage(pagination.page + 1)}
              id="pagination-next"
            >
              Next →
            </button>
          </div>
        </div>
      )}

      {/* Activity feed */}
      <div style={{ marginTop: 'var(--space-xl)' }}>
        <ActivityFeed tasks={tasks} />
      </div>

      {/* Modals */}
      {showModal && (
        <TaskModal
          task={editingTask}
          onSave={handleSave}
          onClose={closeModal}
        />
      )}
      {deletingTask && (
        <ConfirmDialog
          task={deletingTask}
          onConfirm={handleDeleteConfirm}
          onCancel={() => setDeletingTask(null)}
          deleting={isDeleting}
        />
      )}
    </main>
  );
}
