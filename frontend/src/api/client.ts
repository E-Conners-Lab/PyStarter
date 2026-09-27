import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Attach access token to requests
client.interceptors.request.use((config) => {
  const tokens = localStorage.getItem('tokens');
  if (tokens) {
    const { access } = JSON.parse(tokens);
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// Handle token refresh on 401
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const tokens = localStorage.getItem('tokens');
      if (tokens) {
        try {
          const { refresh } = JSON.parse(tokens);
          const res = await axios.post(`${API_BASE}/accounts/token/refresh/`, {
            refresh,
          });
          const newTokens = { access: res.data.access, refresh: res.data.refresh };
          localStorage.setItem('tokens', JSON.stringify(newTokens));
          originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
          return client(originalRequest);
        } catch {
          localStorage.removeItem('tokens');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default client;
