/**
 * ActivityFeed – simulated activity stream
 * -----------------------------------------
 * Shows recent task events.  In a production application this
 * would be driven by a real event log table in the database.
 * For the capstone demo this component renders simulated activity
 * derived from the task list – clearly documented as a simulation.
 */

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins  = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days  = Math.floor(diff / 86400000);
  if (mins  < 1)   return 'just now';
  if (mins  < 60)  return `${mins}m ago`;
  if (hours < 24)  return `${hours}h ago`;
  return `${days}d ago`;
}

export default function ActivityFeed({ tasks }) {
  // Derive simulated activity from the most-recently updated tasks.
  // NOTE: This is a simulation. A production system would persist activity events.
  const events = tasks
    .slice(0, 6)
    .map(task => ({
      id:    task.id,
      text:  task.status === 'DONE'
        ? `✅ "${task.title}" was marked as done`
        : task.status === 'IN_PROGRESS'
        ? `🔄 "${task.title}" moved to In Progress`
        : `📋 Task "${task.title}" was created`,
      time:  task.updated_at || task.created_at,
      color: task.status === 'DONE'
        ? 'var(--color-done)'
        : task.status === 'IN_PROGRESS'
        ? 'var(--color-inprogress)'
        : 'var(--color-accent)',
    }));

  return (
    <div>
      <div className="section-header">
        <h3 className="section-title">Recent Activity</h3>
        <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
          Simulated from task updates
        </span>
      </div>
      <div className="activity-feed">
        {events.length === 0 ? (
          <div className="empty-state" style={{ padding: 'var(--space-lg)' }}>
            <div className="empty-state-icon" style={{ fontSize: '1.5rem' }}>📭</div>
            <div className="empty-state-desc">No activity yet</div>
          </div>
        ) : (
          events.map(event => (
            <div key={event.id} className="activity-item">
              <div className="activity-dot" style={{ background: event.color }} />
              <div>
                <div className="activity-text">{event.text}</div>
                <div className="activity-time">{timeAgo(event.time)}</div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
