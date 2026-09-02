"use client"

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api-client';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await apiClient.get('/api/v1/auth/me');
          setUser(userData);
        } catch (error) {
          console.error("Failed to fetch user", error);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  useEffect(() => {
    // Simple route protection
    const publicRoutes = ['/', '/login', '/register'];
    if (!loading && !user && !publicRoutes.includes(pathname || '')) {
      router.push('/login');
    }
    
    // Redirect away from public if logged in
    if (!loading && user && publicRoutes.includes(pathname || '')) {
      router.push('/home');
    }
  }, [user, loading, pathname, router]);

  const login = (token: string, userData: User) => {
    localStorage.setItem('token', token);
    setUser(userData);
    router.push('/home');
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
