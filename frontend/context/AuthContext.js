'use client';
import { createContext, useState, useEffect, useContext } from 'react';
import api from '../lib/api';
import { useRouter } from 'next/navigation';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            // Ideally call an endpoint to get user profile or decode token
            setUser({ isAuthenticated: true });
        }
        setLoading(false);
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post('token/', { username, password });
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            setUser({ username, isAuthenticated: true });
            router.push('/chat');
            return { success: true };
        } catch (error) {
             console.error("Login failed", error);
             return { success: false, error: error.response?.data?.detail || 'Login failed' };
        }
    };

    const register = async (username, email, password) => {
         try {
            await api.post('register/', { username, email, password });
            // Auto login after register
            return await login(username, password);
         } catch (error) {
             console.error("Registration failed", error);
             return { success: false, error: error.response?.data || 'Registration failed' };
         }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
