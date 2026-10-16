/**
 * StatusBadge – coloured badge for task status
 */
export function StatusBadge({ status }) {
  const config = {
    TODO:        { cls: 'badge-todo',       label: 'To Do',       dot: 'var(--color-todo)' },
    IN_PROGRESS: { cls: 'badge-inprogress', label: 'In Progress', dot: 'var(--color-inprogress)' },
    DONE:        { cls: 'badge-done',       label: 'Done',        dot: 'var(--color-done)' },
  };
  const { cls, label, dot } = config[status] || config.TODO;
  return (
    <span className={`badge ${cls}`}>
      <span className="badge-dot" style={{ background: dot }} />
      {label}
    </span>
  );
}

/**
 * PriorityBadge – coloured badge for task priority
 */
export function PriorityBadge({ priority }) {
  const config = {
    LOW:    { cls: 'badge-low',    label: '↓ Low',    icon: '▽' },
    MEDIUM: { cls: 'badge-medium', label: '— Medium', icon: '◇' },
    HIGH:   { cls: 'badge-high',   label: '↑ High',   icon: '△' },
  };
  const { cls, label } = config[priority] || config.MEDIUM;
  return <span className={`badge ${cls}`}>{label}</span>;
}
