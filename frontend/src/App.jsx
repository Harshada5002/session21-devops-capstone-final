/**
 * App.jsx – root application component
 * Handles layout, navigation state, and mobile sidebar toggle.
 */

import { useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import { useTasks } from './hooks/useTasks';

// Simple placeholder page for non-implemented nav items
function PlaceholderPage({ title, icon }) {
  return (
    <main className="content">
      <h1 style={{ marginBottom: 'var(--space-xl)' }}>{icon} {title}</h1>
      <div className="task-table-wrapper">
        <div className="empty-state">
          <div className="empty-state-icon">{icon}</div>
          <div className="empty-state-title">{title}</div>
          <div className="empty-state-desc">
            This section is part of the TaskBoard capstone project scope.<br />
            The Tasks / Dashboard view demonstrates the full CRUD stack.
          </div>
        </div>
      </div>
    </main>
  );
}

export default function App() {
  const [activeNav, setActiveNav] = useState('tasks');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchValue, setSearchValue] = useState('');

  const renderPage = () => {
    switch (activeNav) {
      case 'dashboard': return <Dashboard />;
      case 'tasks':     return <Dashboard />;
      case 'projects':  return <PlaceholderPage title="Projects" icon="📁" />;
      case 'team':      return <PlaceholderPage title="Team" icon="👥" />;
      case 'settings':  return <PlaceholderPage title="Settings" icon="⚙️" />;
      default:          return <Dashboard />;
    }
  };

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 99 }}
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <Sidebar
        activeNav={activeNav}
        onNavChange={(id) => { setActiveNav(id); setSidebarOpen(false); }}
        taskCount={0}
        className={sidebarOpen ? 'open' : ''}
      />

      <div className="main-layout">
        {/* Header */}
        <header className="header">
          {/* Hamburger for mobile */}
          <button
            className="hamburger"
            onClick={() => setSidebarOpen(o => !o)}
            aria-label="Toggle navigation"
            id="hamburger-btn"
          >
            <span /><span /><span />
          </button>

          <div className="header-title">
            {activeNav.charAt(0).toUpperCase() + activeNav.slice(1)}
          </div>

          {/* Search */}
          <div className="search-bar" role="search">
            <span className="search-icon">🔍</span>
            <input
              id="global-search"
              type="search"
              placeholder="Search tasks…"
              value={searchValue}
              onChange={e => setSearchValue(e.target.value)}
              aria-label="Search tasks"
            />
          </div>

          <div className="header-actions">
            <button className="btn btn-ghost btn-icon" aria-label="Notifications" data-tooltip="Notifications">
              🔔
            </button>
            <div className="user-avatar" style={{ cursor: 'pointer' }}>DV</div>
          </div>
        </header>

        {/* Page content */}
        {renderPage()}
      </div>
    </>
  );
}
