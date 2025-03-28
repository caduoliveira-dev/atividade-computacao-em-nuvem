import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost/api',
  withCredentials: true
});

// Interceptor para adicionar o token em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
}

export interface CreateUserData {
  email: string;
  username: string;
  password: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const authService = {
  async login(data: LoginData): Promise<TokenResponse> {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await api.post('/users/token', formData);
    const token = response.data.access_token;
    localStorage.setItem('token', token);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/users/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
  }
};

export const userService = {
  async createUser(data: CreateUserData): Promise<User> {
    const response = await api.post('/users/', data);
    return response.data;
  },

  async getUser(id: number): Promise<User> {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },
}; 