// Define User type
export interface User {
  user_id: string;
  email: string;
  [key: string]: any; // Allow additional properties
}

// We don't directly initialize the auth client here due to Next.js SSR limitations
// The Better Auth client is meant to be used on the client side only
// For server-side operations, we're using direct API calls as implemented below

// Helper functions for authentication
export const signupUser = async (email: string, password: string) => {
  try {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signup failed');
    }

    const data = await response.json();
    // Store token in localStorage or sessionStorage
    if (data.token) {
      localStorage.setItem('auth-token', data.token);
    }

    return data;
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};

export const loginUser = async (email: string, password: string) => {
  try {
    const response = await fetch('/api/auth/signin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    // Store token in localStorage or sessionStorage
    if (data.token) {
      localStorage.setItem('auth-token', data.token);
    }

    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const logoutUser = async () => {
  try {
    // Remove token from localStorage
    localStorage.removeItem('auth-token');

    // Call the signout endpoint
    await fetch('/api/auth/signout', {
      method: 'POST',
    });
  } catch (error) {
    console.error('Logout error:', error);
    // Even if the backend call fails, remove the local token
    localStorage.removeItem('auth-token');
  }
};

export const getCurrentUser = (): User | null => {
  const token = localStorage.getItem('auth-token');
  if (!token) {
    return null;
  }

  // Decode JWT token to get user info
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    const decodedToken = JSON.parse(jsonPayload);

    // Map JWT fields to expected user properties
    return {
      user_id: decodedToken.user_id,
      email: decodedToken.sub, // 'sub' field in JWT contains the email
      ...decodedToken // Include other fields if present
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Get the authentication token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth-token');
  }
  return null;
};

// Set the authentication token in localStorage
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth-token', token);
  }
};

// Remove the authentication token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth-token');
  }
};

// Check if the user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

// Get user info from token (decode JWT without verification)
export const getUserFromToken = (): User | null => {
  const token = getToken();
  if (!token) return null;

  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const decodedToken = JSON.parse(jsonPayload);

    // Map JWT fields to expected user properties
    return {
      user_id: decodedToken.user_id,
      email: decodedToken.sub, // 'sub' field in JWT contains the email
      ...decodedToken // Include other fields if present
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};