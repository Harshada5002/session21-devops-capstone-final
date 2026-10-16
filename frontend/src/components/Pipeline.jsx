/**
 * Pipeline – visual task stage completion indicator
 */

export default function Pipeline({ stats }) {
  if (!stats) return null;

  const stages = [
    { label: 'To Do',       count: stats.todo,        color: 'var(--color-todo)',       icon: '📋' },
    { label: 'In Progress', count: stats.in_progress,  color: 'var(--color-inprogress)', icon: '🔄' },
    { label: 'Done',        count: stats.done,         color: 'var(--color-done)',       icon: '✅' },
  ];

  const total = stats.total || 1; // avoid divide-by-zero

  return (
    <div className="pipeline">
      {stages.map((stage, i) => (
        <div key={stage.label} style={{ display: 'flex', alignItems: 'stretch', flex: 1 }}>
          <div className="pipeline-stage" style={{ flex: 1 }}>
            <div className="pipeline-stage-header">
              <span className="pipeline-stage-label">{stage.label}</span>
              <span style={{ fontSize: '1.125rem' }}>{stage.icon}</span>
            </div>
            <div className="pipeline-stage-count" style={{ color: stage.color }}>
              {stage.count}
            </div>
            <div className="progress-bar-container">
              <div
                className="progress-bar"
                style={{
                  width: `${(stage.count / total) * 100}%`,
                  background: stage.color,
                }}
              />
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: 4 }}>
              {Math.round((stage.count / total) * 100)}% of total
            </div>
          </div>
          {i < stages.length - 1 && (
            <div className="pipeline-arrow">→</div>
          )}
        </div>
      ))}
    </div>
  );
}
