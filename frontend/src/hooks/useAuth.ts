import { useState, useEffect } from 'react';
import { getToken, removeToken, getUserFromToken } from '../lib/auth';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = () => {
    const token = getToken();
    if (token) {
      const userData = getUserFromToken();
      if (userData) {
        setIsAuthenticated(true);
        setUser(userData);
      } else {
        logout();
      }
    } else {
      setIsAuthenticated(false);
      setUser(null);
    }
    setLoading(false);
  };

  const logout = () => {
    removeToken();
    setIsAuthenticated(false);
    setUser(null);
  };

  return {
    isAuthenticated,
    user,
    loading,
    logout,
    checkAuthStatus
  };
};