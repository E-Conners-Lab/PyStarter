import { create } from 'zustand';
import type { AuthTokens, User } from '../api/types';
import * as authApi from '../api/auth';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  tokens: (() => {
    const stored = localStorage.getItem('tokens');
    return stored ? JSON.parse(stored) : null;
  })(),
  isLoading: false,
  isAuthenticated: !!localStorage.getItem('tokens'),

  login: async (username, password) => {
    const tokens = await authApi.login(username, password);
    localStorage.setItem('tokens', JSON.stringify(tokens));
    set({ tokens, isAuthenticated: true });
    await get().loadUser();
  },

  register: async (username, email, password) => {
    const { user, tokens } = await authApi.register(username, email, password);
    localStorage.setItem('tokens', JSON.stringify(tokens));
    set({ user, tokens, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('tokens');
    set({ user: null, tokens: null, isAuthenticated: false });
  },

  loadUser: async () => {
    if (!get().tokens) return;
    set({ isLoading: true });
    try {
      const user = await authApi.getMe();
      set({ user, isLoading: false });
    } catch {
      set({ isLoading: false });
      get().logout();
    }
  },
}));
