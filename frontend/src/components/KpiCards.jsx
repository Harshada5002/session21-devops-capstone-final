/**
 * KPI Cards – dashboard statistics
 */

export default function KpiCards({ stats, loading }) {
  if (loading || !stats) {
    return (
      <div className="kpi-grid">
        {[1,2,3,4].map(i => (
          <div key={i} className="kpi-card" style={{ opacity: 0.5, minHeight: 120 }}>
            <div className="spinner" style={{ width: 24, height: 24, margin: '20px auto' }} />
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      type: 'total',
      icon: '📋',
      value: stats.total,
      label: 'Total Tasks',
      trend: `${stats.completion_rate}% completion rate`,
    },
    {
      type: 'done',
      icon: '✅',
      value: stats.done,
      label: 'Completed',
      trend: `${stats.in_progress} in progress`,
    },
    {
      type: 'progress',
      icon: '🔄',
      value: stats.in_progress,
      label: 'In Progress',
      trend: `${stats.todo} remaining`,
    },
    {
      type: 'overdue',
      icon: '⚠️',
      value: stats.overdue,
      label: 'Overdue',
      trend: `${stats.high_priority} high priority`,
    },
  ];

  return (
    <div className="kpi-grid">
      {cards.map(card => (
        <div key={card.type} className={`kpi-card ${card.type}`}>
          <div className="kpi-header">
            <div>
              <div className="kpi-value">{card.value}</div>
              <div className="kpi-label">{card.label}</div>
            </div>
            <div className="kpi-icon">{card.icon}</div>
          </div>
          <div className="kpi-trend">{card.trend}</div>
          {card.type === 'done' && stats.total > 0 && (
            <div className="progress-bar-container" style={{ marginTop: 'var(--space-sm)' }}>
              <div
                className="progress-bar"
                style={{ width: `${stats.completion_rate}%` }}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
