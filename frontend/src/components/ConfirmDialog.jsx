/**
 * ConfirmDialog – delete confirmation modal
 */

export default function ConfirmDialog({ task, onConfirm, onCancel, deleting }) {
  if (!task) return null;

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onCancel()}>
      <div className="modal confirm-dialog" role="alertdialog" aria-modal="true" aria-labelledby="confirm-title">
        <div className="modal-header">
          <h2 className="modal-title" id="confirm-title">Delete Task</h2>
          <button className="modal-close btn btn-ghost" onClick={onCancel} aria-label="Cancel">✕</button>
        </div>
        <div className="modal-body" style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
          <div className="confirm-icon">🗑️</div>
          <h3 style={{ marginBottom: 'var(--space-sm)' }}>Are you sure?</h3>
          <p className="confirm-message">
            You are about to delete <strong>"{task.title}"</strong>.
            This action cannot be undone.
          </p>
        </div>
        <div className="modal-footer">
          <button
            id="confirm-cancel-btn"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={deleting}
          >
            Cancel
          </button>
          <button
            id="confirm-delete-btn"
            className="btn btn-danger"
            onClick={() => onConfirm(task.id)}
            disabled={deleting}
          >
            {deleting ? '⏳ Deleting…' : '🗑️ Delete Task'}
          </button>
        </div>
      </div>
    </div>
  );
}
