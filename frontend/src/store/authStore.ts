import { create } from 'zustand';
import { AxiosError } from 'axios';
import api from '../services/api';

interface User {
  id: string;
  email: string;
  full_name: string;
  organization_id: string;
  is_superuser: boolean;
  is_active: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  organization_id: string;
}

interface AuthError {
  message: string;
  status?: number;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: AuthError | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: RegisterData) => Promise<void>;
  clearError: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      // Create form data for OAuth2 format
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post<LoginResponse>('/auth/login/access-token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      // Update axios default headers
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Fetch user data
      const userResponse = await api.get<User>('/users/me');
      set({
        token: access_token,
        user: userResponse.data,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const axiosError = error as AxiosError<{ detail: string }>;
      set({
        isLoading: false,
        error: {
          message: axiosError.response?.data?.detail || 'Failed to login',
          status: axiosError.response?.status,
        },
      });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null,
    });
  },

  register: async (userData: RegisterData) => {
    set({ isLoading: true, error: null });
    try {
      await api.post<User>('/auth/register', userData);
      set({ isLoading: false });
    } catch (error) {
      const axiosError = error as AxiosError<{ detail: string }>;
      set({
        isLoading: false,
        error: {
          message: axiosError.response?.data?.detail || 'Failed to register',
          status: axiosError.response?.status,
        },
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));

export default useAuthStore; 