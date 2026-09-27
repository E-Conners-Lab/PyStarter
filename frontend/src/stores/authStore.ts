import axios from 'axios';
import { create } from 'zustand';
import type { User } from '../api/types';
import * as authApi from '../api/auth';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  login: async (username, password) => {
    const user = await authApi.login(username, password);
    set({ user, isAuthenticated: true });
  },

  register: async (username, password) => {
    const { user } = await authApi.register(username, password);
    set({ user, isAuthenticated: true });
  },

  logout: () => {
    authApi.logout().catch(() => {});
    set({ user: null, isAuthenticated: false });
  },

  loadUser: async () => {
    set({ isLoading: true });
    try {
      const user = await authApi.getMe();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (err) {
      set({ isLoading: false });
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        set({ isAuthenticated: false, user: null });
      }
    }
  },
}));
