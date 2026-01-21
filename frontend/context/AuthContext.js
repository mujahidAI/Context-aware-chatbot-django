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
            // Attempt to register the user
            const response = await api.post('register/', { username, email, password });
            
            // Only if registration succeeds, attempt to login
            if (response.status === 201 || response.status === 200) {
                return await login(username, password);
            }
            
            return { success: false, error: 'Registration failed' };
         } catch (error) {
             console.error("Registration failed", error);
             
             // Format error messages from backend
             let errorMessage = 'Registration failed';
             
             if (error.response?.data) {
                 const errorData = error.response.data;
                 
                 // Handle field-specific errors
                 if (typeof errorData === 'object') {
                     const errors = [];
                     for (const [field, messages] of Object.entries(errorData)) {
                         if (Array.isArray(messages)) {
                             errors.push(...messages);
                         } else {
                             errors.push(messages);
                         }
                     }
                     errorMessage = errors.join('. ');
                 } else if (typeof errorData === 'string') {
                     errorMessage = errorData;
                 }
             }
             
             // Return error WITHOUT attempting to login
             return { success: false, error: errorMessage };
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
