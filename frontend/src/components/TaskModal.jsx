/**
 * TaskModal – create and edit tasks
 */

import { useState, useEffect } from 'react';

const DEFAULT_FORM = {
  title: '',
  description: '',
  status: 'TODO',
  priority: 'MEDIUM',
  assignee: '',
  due_date: '',
};

export default function TaskModal({ task, onSave, onClose }) {
  const isEdit = Boolean(task);
  const [form, setForm] = useState(DEFAULT_FORM);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (task) {
      setForm({
        title:       task.title       || '',
        description: task.description || '',
        status:      task.status      || 'TODO',
        priority:    task.priority    || 'MEDIUM',
        assignee:    task.assignee    || '',
        due_date:    task.due_date
          ? task.due_date.slice(0, 16)   // format for datetime-local input
          : '',
      });
    } else {
      setForm(DEFAULT_FORM);
    }
    setErrors({});
  }, [task]);

  const set = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }));
    setErrors(prev => ({ ...prev, [key]: undefined }));
  };

  const validate = () => {
    const errs = {};
    if (!form.title.trim()) errs.title = 'Title is required';
    if (form.title.length > 255) errs.title = 'Title must be ≤ 255 characters';
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }

    setSaving(true);
    try {
      const payload = { ...form };
      if (!payload.description) delete payload.description;
      if (!payload.assignee)    delete payload.assignee;
      if (!payload.due_date)    delete payload.due_date;
      else payload.due_date = new Date(payload.due_date).toISOString();

      await onSave(payload);
      onClose();
    } catch (err) {
      setErrors({ general: err.message || 'Save failed. Please try again.' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-header">
          <h2 className="modal-title" id="modal-title">
            {isEdit ? '✏️ Edit Task' : '✨ Create Task'}
          </h2>
          <button
            className="modal-close btn btn-ghost"
            onClick={onClose}
            aria-label="Close modal"
            id="modal-close-btn"
          >✕</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {errors.general && (
              <div className="error-banner" style={{ marginBottom: 'var(--space-md)' }}>
                ⚠️ {errors.general}
              </div>
            )}

            {/* Title */}
            <div className="form-group">
              <label className="form-label" htmlFor="task-title">
                Title <span className="required">*</span>
              </label>
              <input
                id="task-title"
                className="form-input"
                placeholder="e.g. Design the login page"
                value={form.title}
                onChange={e => set('title', e.target.value)}
                maxLength={255}
                autoFocus
              />
              {errors.title && <div className="form-error">{errors.title}</div>}
            </div>

            {/* Description */}
            <div className="form-group">
              <label className="form-label" htmlFor="task-desc">Description</label>
              <textarea
                id="task-desc"
                className="form-textarea"
                placeholder="Describe the task in detail…"
                value={form.description}
                onChange={e => set('description', e.target.value)}
                rows={3}
              />
            </div>

            {/* Status + Priority */}
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="task-status">Status</label>
                <select
                  id="task-status"
                  className="form-select"
                  value={form.status}
                  onChange={e => set('status', e.target.value)}
                >
                  <option value="TODO">To Do</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="DONE">Done</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="task-priority">Priority</label>
                <select
                  id="task-priority"
                  className="form-select"
                  value={form.priority}
                  onChange={e => set('priority', e.target.value)}
                >
                  <option value="LOW">↓ Low</option>
                  <option value="MEDIUM">— Medium</option>
                  <option value="HIGH">↑ High</option>
                </select>
              </div>
            </div>

            {/* Assignee + Due date */}
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="task-assignee">Assignee</label>
                <input
                  id="task-assignee"
                  className="form-input"
                  placeholder="e.g. Alice"
                  value={form.assignee}
                  onChange={e => set('assignee', e.target.value)}
                  maxLength={255}
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="task-due">Due Date</label>
                <input
                  id="task-due"
                  type="datetime-local"
                  className="form-input"
                  value={form.due_date}
                  onChange={e => set('due_date', e.target.value)}
                  style={{ colorScheme: 'dark' }}
                />
              </div>
            </div>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              id="modal-cancel-btn"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={saving}
              id="modal-save-btn"
            >
              {saving ? '⏳ Saving…' : isEdit ? '💾 Save Changes' : '✨ Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
