// API service to handle requests with JWT authorization
class ApiService {
  private baseUrl: string;
  private token: string | null;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.token = typeof window !== 'undefined' ? localStorage.getItem('auth-token') : null;
  }

  // Update token when it changes (e.g., after login)
  public setToken(token: string | null) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('auth-token', token);
      } else {
        localStorage.removeItem('auth-token');
      }
    }
  }

  // Get token from localStorage
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth-token');
    }
    return null;
  }

  // Generic request method that includes authorization header
  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers as Record<string, string>,
    };

    // Add authorization header if token exists
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
      headers,
      ...options,
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized responses
      if (response.status === 401) {
        // Remove invalid token
        this.setToken(null);

        // Optionally redirect to login
        if (typeof window !== 'undefined') {
          // window.location.href = '/signin'; // Uncomment if auto-redirect is desired
        }

        throw new Error('Unauthorized: Invalid or expired token');
      }

      // Attempt to parse response as JSON
      const contentType = response.headers.get('content-type');
      let data;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        // FastAPI validation errors use 'detail' field, not 'message'
        const errorMessage = data.detail || data.message || `HTTP error! status: ${response.status}`;

        // Log full error details for debugging
        console.error('API Error Details:', {
          status: response.status,
          statusText: response.statusText,
          data: data
        });

        throw new Error(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
      }

      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // GET request
  public async get<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'GET' });
  }

  // POST request
  public async post<T>(endpoint: string, body: any): Promise<T> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  // PUT request
  public async put<T>(endpoint: string, body: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  // DELETE request
  public async delete<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'DELETE' });
  }

  // PATCH request
  public async patch<T>(endpoint: string, body: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    });
  }
}

// Create singleton instance
export const apiService = new ApiService();

export default ApiService;