import axios from 'axios';

declare global {
  interface ImportMeta {
    env: {
      VITE_API_URL: string;
    };
  }
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    } else if (error.response?.status === 403) {
      // Handle forbidden access
      console.error('Forbidden access:', error.response?.data);
    } else if (error.response?.status === 404) {
      // Handle not found
      console.error('Resource not found:', error.response?.data);
    } else if (error.response?.status >= 500) {
      // Handle server errors
      console.error('Server error:', error.response?.data);
    } else if (error.code === 'ECONNABORTED') {
      // Handle timeout
      console.error('Request timeout');
    } else {
      // Handle other errors
      console.error('API error:', error);
    }
    return Promise.reject(error);
  }
);

export default api; 