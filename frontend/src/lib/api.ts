import { getToken } from './auth';

// Base API client with JWT handling
const apiClient = {
  get: async (endpoint: string) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Fallback to default
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
    });

    // Check if response is JSON before parsing to avoid "Unexpected token '<'" error
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();

      // If it's an error response that's not JSON, throw a descriptive error
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${response.statusText}. Received: ${text.substring(0, 200)}...`);
      }

      // If it's a successful response but not JSON, try to parse it anyway
      try {
        return JSON.parse(text);
      } catch (e) {
        // If it's not JSON and we can't parse it, throw an error
        throw new Error(`Expected JSON response but got: ${text.substring(0, 200)}...`);
      }
    }

    if (!response.ok) {
      // Try to get error details from response if possible
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage += `, message: ${errorData.message || errorData.detail || 'Unknown error'}`;
      } catch (e) {
        // If error response is not JSON, use status text
        errorMessage += `, message: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  post: async (endpoint: string, data: any) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Fallback to default
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    // Check if response is JSON before parsing to avoid "Unexpected token '<'" error
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();

      // If it's an error response that's not JSON, throw a descriptive error
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${response.statusText}. Received: ${text.substring(0, 200)}...`);
      }

      // If it's a successful response but not JSON, try to parse it anyway
      try {
        return JSON.parse(text);
      } catch (e) {
        // If it's not JSON and we can't parse it, throw an error
        throw new Error(`Expected JSON response but got: ${text.substring(0, 200)}...`);
      }
    }

    if (!response.ok) {
      // Try to get error details from response if possible
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage += `, message: ${errorData.message || errorData.detail || 'Unknown error'}`;
      } catch (e) {
        // If error response is not JSON, use status text
        errorMessage += `, message: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  put: async (endpoint: string, data: any) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Fallback to default
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    // Check if response is JSON before parsing to avoid "Unexpected token '<'" error
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();

      // If it's an error response that's not JSON, throw a descriptive error
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${response.statusText}. Received: ${text.substring(0, 200)}...`);
      }

      // If it's a successful response but not JSON, try to parse it anyway
      try {
        return JSON.parse(text);
      } catch (e) {
        // If it's not JSON and we can't parse it, throw an error
        throw new Error(`Expected JSON response but got: ${text.substring(0, 200)}...`);
      }
    }

    if (!response.ok) {
      // Try to get error details from response if possible
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage += `, message: ${errorData.message || errorData.detail || 'Unknown error'}`;
      } catch (e) {
        // If error response is not JSON, use status text
        errorMessage += `, message: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  patch: async (endpoint: string, data: any) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Fallback to default
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    // Check if response is JSON before parsing to avoid "Unexpected token '<'" error
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();

      // If it's an error response that's not JSON, throw a descriptive error
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${response.statusText}. Received: ${text.substring(0, 200)}...`);
      }

      // If it's a successful response but not JSON, try to parse it anyway
      try {
        return JSON.parse(text);
      } catch (e) {
        // If it's not JSON and we can't parse it, throw an error
        throw new Error(`Expected JSON response but got: ${text.substring(0, 200)}...`);
      }
    }

    if (!response.ok) {
      // Try to get error details from response if possible
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage += `, message: ${errorData.message || errorData.detail || 'Unknown error'}`;
      } catch (e) {
        // If error response is not JSON, use status text
        errorMessage += `, message: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  delete: async (endpoint: string) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Fallback to default
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
    });

    // Check if response is JSON before parsing to avoid "Unexpected token '<'" error
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();

      // If it's an error response that's not JSON, throw a descriptive error
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, message: ${response.statusText}. Received: ${text.substring(0, 200)}...`);
      }

      // If it's a successful response but not JSON, try to parse it anyway
      try {
        return JSON.parse(text);
      } catch (e) {
        // If it's not JSON and we can't parse it, throw an error
        throw new Error(`Expected JSON response but got: ${text.substring(0, 200)}...`);
      }
    }

    if (!response.ok) {
      // Try to get error details from response if possible
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage += `, message: ${errorData.message || errorData.detail || 'Unknown error'}`;
      } catch (e) {
        // If error response is not JSON, use status text
        errorMessage += `, message: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }
};

// Specific API functions for todos
export const todoApi = {
  getTodos: () => apiClient.get('/api/todos'),
  createTodo: (todo: { title: string; description?: string }) =>
    apiClient.post('/api/todos', todo),
  updateTodo: (id: string, todo: { title?: string; description?: string; completed?: boolean }) =>
    apiClient.put(`/api/todos/${id}`, todo),
  toggleTodoCompletion: (id: string, completed: boolean) =>
    apiClient.patch(`/api/todos/${id}/complete`, { completed }),
  deleteTodo: (id: string) => apiClient.delete(`/api/todos/${id}`),
  getTodoById: (id: string) => apiClient.get(`/api/todos/${id}`)
};

export default apiClient;