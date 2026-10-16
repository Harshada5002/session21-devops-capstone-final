/**
 * Sidebar navigation component
 */

import { useState } from 'react';

const NAV_ITEMS = [
  { icon: '⬛', label: 'Dashboard', id: 'dashboard' },
  { icon: '✅', label: 'Tasks',     id: 'tasks',     badge: null },
  { icon: '📁', label: 'Projects',  id: 'projects' },
  { icon: '👥', label: 'Team',      id: 'team' },
  { icon: '⚙️', label: 'Settings',  id: 'settings' },
];

export default function Sidebar({ activeNav, onNavChange, taskCount }) {
  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">⚡</div>
        <span className="sidebar-logo-text">TaskBoard</span>
      </div>

      {/* Workspace selector */}
      <div className="sidebar-workspace">
        <div>
          <div className="sidebar-workspace-name">Dev Team Workspace</div>
          <div className="sidebar-workspace-plan">Pro Plan</div>
        </div>
        <span style={{ color: 'var(--color-text-muted)', fontSize:'0.75rem' }}>⌄</span>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="sidebar-nav-section-label">Main Menu</div>
        {NAV_ITEMS.map(item => (
          <div
            key={item.id}
            className={`nav-item ${activeNav === item.id ? 'active' : ''}`}
            onClick={() => onNavChange(item.id)}
            role="button"
            tabIndex={0}
            onKeyDown={e => e.key === 'Enter' && onNavChange(item.id)}
            id={`nav-${item.id}`}
          >
            <span className="nav-item-icon">{item.icon}</span>
            <span>{item.label}</span>
            {item.id === 'tasks' && taskCount > 0 && (
              <span className="nav-item-badge">{taskCount}</span>
            )}
          </div>
        ))}

        <div className="sidebar-nav-section-label" style={{ marginTop: 'var(--space-md)' }}>
          Quick Actions
        </div>
        <div className="nav-item">
          <span className="nav-item-icon">📊</span>
          <span>Reports</span>
        </div>
        <div className="nav-item">
          <span className="nav-item-icon">🔔</span>
          <span>Notifications</span>
        </div>
      </nav>

      {/* User footer */}
      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="user-avatar">DV</div>
          <div className="user-info">
            <div className="user-name">Dev User</div>
            <div className="user-role">Admin</div>
          </div>
          <span style={{ color: 'var(--color-text-muted)', fontSize:'0.75rem' }}>⋮</span>
        </div>
      </div>
    </aside>
  );
}
