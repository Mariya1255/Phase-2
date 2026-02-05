// API client wrapper with token inclusion
import { apiService } from './api';

/**
 * API Client that wraps the ApiService to provide specific endpoints
 */
class ApiClient {
  // Protected endpoint example
  static async getProtectedData() {
    try {
      const response = await apiService.get<{ message: string; user_id: string; email: string }>('/api/protected/protected-data');
      return response;
    } catch (error) {
      console.error('Error fetching protected data:', error);
      throw error;
    }
  }

  static async getDashboardData() {
    try {
      const response = await apiService.get<any>('/api/protected/dashboard');
      return response;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  }

  // Method to set token (called after login)
  static setToken(token: string | null) {
    apiService.setToken(token);
  }

  // Method to get current token
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth-token');
    }
    return null;
  }

  // Generic methods for flexibility
  static async get<T>(endpoint: string): Promise<T> {
    return apiService.get<T>(endpoint);
  }

  static async post<T>(endpoint: string, body: any): Promise<T> {
    return apiService.post<T>(endpoint, body);
  }

  static async put<T>(endpoint: string, body: any): Promise<T> {
    return apiService.put<T>(endpoint, body);
  }

  static async delete<T>(endpoint: string): Promise<T> {
    return apiService.delete<T>(endpoint);
  }
}

export default ApiClient;