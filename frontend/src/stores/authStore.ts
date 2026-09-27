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
  authError: string | null;
  logout: () => Promise<void>;
  clearSession: () => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  authError: null,

  login: async (username, password) => {
    const user = await authApi.login(username, password);
    set({ user, isAuthenticated: true, authError: null });
  },

  register: async (username, password) => {
    const { user } = await authApi.register(username, password);
    set({ user, isAuthenticated: true, authError: null });
  },

  clearSession: () => set({ user: null, isAuthenticated: false, isLoading: false }),

  logout: async () => {
    try {
      await authApi.logout();
      set({ user: null, isAuthenticated: false, authError: null });
    } catch {
      set({ authError: "Sign out failed. Please try again." });
    }
  },

  loadUser: async () => {
    // Refreshing XP must not unmount protected pages and discard their results.
    set((state) => ({ isLoading: !state.isAuthenticated }));
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
