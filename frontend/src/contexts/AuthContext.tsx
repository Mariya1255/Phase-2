'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  user_id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
  refreshUser: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const decodeToken = (token: string): User | null => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      const decoded = JSON.parse(jsonPayload);
      return {
        user_id: decoded.user_id,
        email: decoded.sub,
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };

  const refreshUser = () => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      const userData = decodeToken(token);
      setUser(userData);
    } else {
      setUser(null);
    }
  };

  useEffect(() => {
    refreshUser();
    setIsLoading(false);
  }, []);

  // Route protection logic
  useEffect(() => {
    if (isLoading) return;

    const token = localStorage.getItem('auth-token');
    const isAuthPage = pathname?.startsWith('/auth');
    const isDashboard = pathname?.startsWith('/dashboard');

    // Redirect to signin if accessing dashboard without token
    if (isDashboard && !token) {
      router.push('/auth/sign-in');
    }

    // Redirect to dashboard if accessing auth pages with token
    if (isAuthPage && token) {
      router.push('/dashboard/tasks');
    }
  }, [pathname, isLoading, router]);

  const login = (token: string) => {
    localStorage.setItem('auth-token', token);
    const userData = decodeToken(token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('auth-token');
    setUser(null);
    router.push('/');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
