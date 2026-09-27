import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

// Handle token refresh on 401
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(
          `${API_BASE}/accounts/token/refresh/`,
          {},
          { withCredentials: true },
        );
        if (res.data?.status === 'refreshed') {
          return client(originalRequest);
        }
        // Refresh response invalid — treat as failed
        const { useAuthStore } = await import('../stores/authStore');
        useAuthStore.getState().logout();
      } catch {
        const { useAuthStore } = await import('../stores/authStore');
        useAuthStore.getState().logout();
      }
    }
    return Promise.reject(error);
  }
);

export default client;
