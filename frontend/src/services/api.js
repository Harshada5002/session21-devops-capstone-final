/**
 * API service layer
 * -----------------
 * All backend communication lives here.
 * Components never call fetch() directly.
 *
 * The base URL is read from the Vite environment variable
 * VITE_API_BASE_URL, falling back to an empty string so that
 * requests use the same origin (works with the Vite dev proxy
 * and the Nginx reverse-proxy in production).
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

/** Generic fetch wrapper with error handling. */
async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });

  if (response.status === 204) return null; // DELETE success

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(message);
  }

  return data;
}

// ── Task API ──────────────────────────────────────────────────────────────────

/**
 * Fetch a paginated, filtered list of tasks.
 * @param {Object} params - { status, priority, search, page, page_size }
 */
export async function fetchTasks(params = {}) {
  const qs = new URLSearchParams();
  if (params.status)    qs.set('status', params.status);
  if (params.priority)  qs.set('priority', params.priority);
  if (params.search)    qs.set('search', params.search);
  if (params.page)      qs.set('page', params.page);
  if (params.page_size) qs.set('page_size', params.page_size);
  const query = qs.toString() ? `?${qs}` : '';
  return apiFetch(`/api/tasks${query}`);
}

/** Fetch a single task by ID. */
export async function fetchTask(id) {
  return apiFetch(`/api/tasks/${id}`);
}

/**
 * Create a new task.
 * @param {Object} payload - TaskCreate fields
 */
export async function createTask(payload) {
  return apiFetch('/api/tasks', { method: 'POST', body: JSON.stringify(payload) });
}

/**
 * Update an existing task.
 * @param {number} id - Task ID
 * @param {Object} payload - Partial TaskUpdate fields
 */
export async function updateTask(id, payload) {
  return apiFetch(`/api/tasks/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
}

/** Delete a task by ID. */
export async function deleteTask(id) {
  return apiFetch(`/api/tasks/${id}`, { method: 'DELETE' });
}

/** Fetch dashboard statistics. */
export async function fetchStats() {
  return apiFetch('/api/tasks/stats');
}

// ── Health ────────────────────────────────────────────────────────────────────

export async function checkHealth() {
  return apiFetch('/health');
}
