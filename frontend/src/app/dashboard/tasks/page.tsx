'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
  user_id: string;
}

type FilterType = 'all' | 'active' | 'completed';

// Skeleton Loader Component
const TaskSkeleton = () => (
  <div className="bg-[#1A1A1B] border border-white/5 rounded-xl p-5 animate-pulse">
    <div className="flex items-start gap-4">
      <div className="w-5 h-5 bg-white/10 rounded"></div>
      <div className="flex-1 space-y-3">
        <div className="h-5 bg-white/10 rounded w-3/4"></div>
        <div className="h-4 bg-white/10 rounded w-1/2"></div>
      </div>
    </div>
  </div>
);

// Empty State Component
const EmptyState = ({ onCreateTask }: { onCreateTask: () => void }) => (
  <div className="flex flex-col items-center justify-center py-20 px-4">
    <svg
      className="w-32 h-32 mb-6 text-gray-600"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
      />
    </svg>
    <h3 className="text-xl font-semibold text-white mb-2">No tasks yet</h3>
    <p className="text-gray-400 text-center mb-6 max-w-sm">
      Create your first task to get started with your productivity journey
    </p>
    <button
      onClick={onCreateTask}
      className="px-6 py-3 bg-[#0070F3] hover:bg-[#0060D9] text-white rounded-lg font-medium transition-all shadow-lg shadow-[#0070F3]/20 hover:shadow-[#0070F3]/30"
    >
      Create Your First Task
    </button>
  </div>
);

// Confirm Delete Modal
const ConfirmDeleteModal = ({
  onConfirm,
  onCancel,
  loading,
}: {
  onConfirm: () => void;
  onCancel: () => void;
  loading: boolean;
}) => (
  <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div className="bg-[#1A1A1B] border border-white/10 rounded-2xl p-6 w-full max-w-md shadow-2xl">
      <div className="flex items-center gap-4 mb-4">
        <div className="w-12 h-12 bg-red-500/10 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">Delete Task</h3>
          <p className="text-sm text-gray-400">This action cannot be undone</p>
        </div>
      </div>
      <p className="text-gray-300 mb-6">
        Are you sure you want to delete this task? This will permanently remove it from your list.
      </p>
      <div className="flex gap-3">
        <button
          onClick={onCancel}
          disabled={loading}
          className="flex-1 px-4 py-2.5 bg-white/5 hover:bg-white/10 text-white rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          onClick={onConfirm}
          disabled={loading}
          className="flex-1 px-4 py-2.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  </div>
);

// Relative Time Helper
const getRelativeTime = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
};

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filter, setFilter] = useState<FilterType>('all');
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
  });
  const [error, setError] = useState<string>('');
  const [createLoading, setCreateLoading] = useState(false);
  const [deleteTaskId, setDeleteTaskId] = useState<string | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth-token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error('Failed to fetch tasks');

      const data: Task[] = await response.json();
      setTasks(data);
    } catch (err: any) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.title.trim()) {
      setError('Task title is required');
      return;
    }

    setCreateLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('auth-token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          status: 'pending',
        }),
      });

      if (!response.ok) throw new Error('Failed to create task');

      const createdTask: Task = await response.json();
      setTasks([createdTask, ...tasks]);
      setNewTask({ title: '', description: '' });
      setShowCreateModal(false);
    } catch (err: any) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    } finally {
      setCreateLoading(false);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    // Optimistic update
    const newStatus: 'pending' | 'in_progress' | 'completed' =
      task.status === 'completed' ? 'pending' : 'completed';
    const optimisticTasks = tasks.map((t) =>
      t.id === task.id ? { ...t, status: newStatus } : t
    );
    setTasks(optimisticTasks);

    try {
      const token = localStorage.getItem('auth-token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: task.title,
          description: task.description,
          status: newStatus,
        }),
      });

      if (!response.ok) {
        // Revert on error
        setTasks(tasks);
        throw new Error('Failed to update task');
      }

      const updatedTask: Task = await response.json();
      setTasks(tasks.map((t) => (t.id === task.id ? updatedTask : t)));
    } catch (err: any) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async () => {
    if (!deleteTaskId) return;

    setDeleteLoading(true);

    try {
      const token = localStorage.getItem('auth-token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${deleteTaskId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error('Failed to delete task');

      setTasks(tasks.filter((task) => task.id !== deleteTaskId));
      setDeleteTaskId(null);
    } catch (err: any) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setDeleteLoading(false);
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === 'active') return task.status !== 'completed';
    if (filter === 'completed') return task.status === 'completed';
    return true;
  });

  const filters: { label: string; value: FilterType }[] = [
    { label: 'All', value: 'all' },
    { label: 'Active', value: 'active' },
    { label: 'Completed', value: 'completed' },
  ];

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 pb-24 md:pb-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Tasks</h1>
        <p className="text-gray-400">Manage your tasks and stay productive</p>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center gap-3 mb-6 overflow-x-auto pb-2">
        {filters.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap transition-all ${
              filter === f.value
                ? 'bg-[#0070F3] text-white shadow-lg shadow-[#0070F3]/20'
                : 'bg-[#1A1A1B] text-gray-400 hover:text-white hover:bg-white/5 border border-white/5'
            }`}
          >
            {f.label}
          </button>
        ))}
        <button
          onClick={() => setShowCreateModal(true)}
          className="ml-auto px-4 py-2 bg-[#0070F3] hover:bg-[#0060D9] text-white rounded-lg font-medium text-sm transition-all shadow-lg shadow-[#0070F3]/20 hover:shadow-[#0070F3]/30"
        >
          + New Task
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm flex items-center justify-between">
          <span>{error}</span>
          <button onClick={() => setError('')} className="text-red-400 hover:text-red-300">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Task List */}
      <div className="space-y-3">
        {loading ? (
          <>
            <TaskSkeleton />
            <TaskSkeleton />
            <TaskSkeleton />
          </>
        ) : filteredTasks.length === 0 ? (
          <EmptyState onCreateTask={() => setShowCreateModal(true)} />
        ) : (
          filteredTasks.map((task) => (
            <div
              key={task.id}
              className="group bg-[#1A1A1B] border border-white/5 rounded-xl p-5 hover:border-white/10 transition-all hover:shadow-lg hover:shadow-black/20"
            >
              <div className="flex items-start gap-4">
                {/* Checkbox */}
                <button
                  onClick={() => handleToggleComplete(task)}
                  className={`mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                    task.status === 'completed'
                      ? 'bg-[#0070F3] border-[#0070F3]'
                      : 'border-gray-600 hover:border-[#0070F3]'
                  }`}
                >
                  {task.status === 'completed' && (
                    <svg
                      className="w-3 h-3 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={3}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  )}
                </button>

                {/* Task Content */}
                <div className="flex-1 min-w-0">
                  <h3
                    className={`text-base font-medium mb-1 ${
                      task.status === 'completed'
                        ? 'text-gray-500 line-through'
                        : 'text-white'
                    }`}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p
                      className={`text-sm mb-2 ${
                        task.status === 'completed'
                          ? 'text-gray-600'
                          : 'text-gray-400'
                      }`}
                    >
                      {task.description}
                    </p>
                  )}
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    <span>{getRelativeTime(task.updated_at)}</span>
                    <span
                      className={`px-2 py-1 rounded-full border font-medium ${
                        task.status === 'completed'
                          ? 'bg-green-500/10 text-green-400 border-green-500/20'
                          : task.status === 'in_progress'
                          ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
                          : 'bg-gray-500/10 text-gray-400 border-gray-500/20'
                      }`}
                    >
                      {task.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => setDeleteTaskId(task.id)}
                    className="p-2 hover:bg-red-500/10 rounded-lg transition-all"
                  >
                    <svg
                      className="w-4 h-4 text-gray-400 hover:text-red-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Create Task Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-[#1A1A1B] border border-white/10 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h2 className="text-xl font-semibold text-white mb-4">
              Create New Task
            </h2>
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  value={newTask.title}
                  onChange={(e) =>
                    setNewTask({ ...newTask, title: e.target.value })
                  }
                  disabled={createLoading}
                  className="w-full bg-[#0A0A0B] border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-[#0070F3] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="Enter task title"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Description
                </label>
                <textarea
                  value={newTask.description}
                  onChange={(e) =>
                    setNewTask({ ...newTask, description: e.target.value })
                  }
                  disabled={createLoading}
                  rows={3}
                  className="w-full bg-[#0A0A0B] border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-[#0070F3] transition-colors resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                  placeholder="Enter task description (optional)"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  disabled={createLoading}
                  className="flex-1 px-4 py-2.5 bg-white/5 hover:bg-white/10 text-white rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createLoading}
                  className="flex-1 px-4 py-2.5 bg-[#0070F3] hover:bg-[#0060D9] text-white rounded-lg font-medium transition-all shadow-lg shadow-[#0070F3]/20 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {createLoading ? 'Creating...' : 'Create Task'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Confirm Delete Modal */}
      {deleteTaskId && (
        <ConfirmDeleteModal
          onConfirm={handleDeleteTask}
          onCancel={() => setDeleteTaskId(null)}
          loading={deleteLoading}
        />
      )}
    </div>
  );
}
