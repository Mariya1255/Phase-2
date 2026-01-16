'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { todoApi } from '../../../../lib/api';
import { useAuth } from '../../../../hooks/useAuth';
import ProtectedRoute from '../../../../components/ProtectedRoute';

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TodoDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [todo, setTodo] = useState<Todo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTodo();
  }, [id]);

  const fetchTodo = async () => {
    try {
      setLoading(true);
      const data = await todoApi.getTodoById(id as string);
      setTodo(data);
    } catch (err) {
      setError('Failed to fetch todo');
      console.error('Error fetching todo:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleCompletion = async () => {
    if (!todo) return;

    try {
      await todoApi.toggleTodoCompletion(todo.id, !todo.completed);
      setTodo({
        ...todo,
        completed: !todo.completed
      });
    } catch (err) {
      setError('Failed to update todo');
      console.error('Error updating todo:', err);
    }
  };

  const handleDelete = async () => {
    if (!todo) return;

    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await todoApi.deleteTodo(todo.id);
        router.push('/dashboard');
      } catch (err) {
        setError('Failed to delete todo');
        console.error('Error deleting todo:', err);
      }
    }
  };

  if (loading) return <div className="text-center py-8">Loading todo...</div>;

  if (error) return <div className="text-center py-8 text-red-500">{error}</div>;

  if (!todo) return <div className="text-center py-8">Todo not found</div>;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-semibold text-gray-900">Todo App</h1>
              </div>
              <div className="flex items-center">
                <span className="text-sm text-gray-700 mr-4">
                  Welcome, {user?.email || 'User'}
                </span>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <div className="max-w-2xl mx-auto p-4">
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-start">
                <h1 className="text-2xl font-bold text-gray-900 mb-4">Todo Details</h1>
                <button
                  onClick={() => router.back()}
                  className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Back
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <h2 className="text-lg font-medium text-gray-900">Title</h2>
                  <p className={`mt-1 text-gray-600 ${todo.completed ? 'line-through text-gray-500' : ''}`}>
                    {todo.title}
                  </p>
                </div>

                {todo.description && (
                  <div>
                    <h2 className="text-lg font-medium text-gray-900">Description</h2>
                    <p className={`mt-1 text-gray-600 ${todo.completed ? 'line-through text-gray-500' : ''}`}>
                      {todo.description}
                    </p>
                  </div>
                )}

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={toggleCompletion}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 block text-sm text-gray-900">
                    {todo.completed ? 'Completed' : 'Mark as complete'}
                  </label>
                </div>

                <div className="text-sm text-gray-500">
                  <p>Created: {new Date(todo.created_at).toLocaleString()}</p>
                  <p>Updated: {new Date(todo.updated_at).toLocaleString()}</p>
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={handleDelete}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Delete
                  </button>

                  <button
                    onClick={() => router.push('/dashboard')}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Back to Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}