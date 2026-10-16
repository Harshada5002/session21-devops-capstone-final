/**
 * useTasks hook
 * -------------
 * Manages the task list state, filtering, pagination,
 * and CRUD operations.  Components call this hook rather
 * than fetching data directly.
 */

import { useState, useEffect, useCallback } from 'react';
import { fetchTasks, fetchStats, createTask, updateTask, deleteTask } from '../services/api';

export function useTasks() {
  const [tasks, setTasks]       = useState([]);
  const [stats, setStats]       = useState(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [pagination, setPagination] = useState({ total: 0, page: 1, pages: 1 });

  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
    page: 1,
    page_size: 20,
  });

  const loadTasks = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      const [taskData, statsData] = await Promise.all([
        fetchTasks(params),
        fetchStats(),
      ]);
      setTasks(taskData.items);
      setPagination({ total: taskData.total, page: taskData.page, pages: taskData.pages });
      setStats(statsData);
    } catch (err) {
      setError(err.message || 'Failed to load tasks. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => { loadTasks(filters); }, [filters]);

  const applyFilter = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }));
  };

  const setPage = (page) => setFilters(prev => ({ ...prev, page }));

  const addTask = async (payload) => {
    const created = await createTask(payload);
    await loadTasks(filters);
    return created;
  };

  const editTask = async (id, payload) => {
    const updated = await updateTask(id, payload);
    await loadTasks(filters);
    return updated;
  };

  const removeTask = async (id) => {
    await deleteTask(id);
    await loadTasks(filters);
  };

  return {
    tasks,
    stats,
    loading,
    error,
    filters,
    pagination,
    applyFilter,
    setPage,
    addTask,
    editTask,
    removeTask,
    reload: () => loadTasks(filters),
  };
}
