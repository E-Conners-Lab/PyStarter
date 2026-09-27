import axios from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';
const options = {
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
};
const transport = axios.create(options);
const client = axios.create(options);
let csrfToken: string | null = null;
let csrfRequest: Promise<string> | null = null;
let refreshRequest: Promise<void> | null = null;

async function getCsrfToken(): Promise<string> {
  if (csrfToken) return csrfToken;
  if (!csrfRequest) {
    csrfRequest = transport.get('/accounts/csrf/').then((response) => {
      csrfToken = response.data.csrfToken;
      if (typeof csrfToken !== 'string') throw new Error('Unable to initialize session.');
      return csrfToken;
    }).finally(() => { csrfRequest = null; });
  }
  return csrfRequest;
}

client.interceptors.request.use(async (config) => {
  if (!['get', 'head', 'options'].includes(config.method || 'get')) {
    return {
      ...config,
      data: config.data === undefined ? {} : config.data,
      headers: config.headers.concat({
        'Content-Type': 'application/json',
        'X-CSRFToken': await getCsrfToken(),
      }),
    };
  }
  return config;
});

async function refreshSession(): Promise<void> {
  if (!refreshRequest) {
    refreshRequest = getCsrfToken().then(async (token) => {
      const response = await transport.post('/accounts/token/refresh/', {}, {
        headers: { 'X-CSRFToken': token },
      });
      if (response.data.status !== 'refreshed') throw new Error('Session expired.');
    }).finally(() => { refreshRequest = null; });
  }
  return refreshRequest;
}

const AUTH_LIFECYCLE = /\/accounts\/(?:login|register|logout|token\/refresh|password-reset|password-reset-confirm)\//;
type RetryConfig = InternalAxiosRequestConfig & { _retry?: boolean };

client.interceptors.response.use(
  (response) => {
    const rotatedToken = response.headers['x-csrftoken'];
    if (typeof rotatedToken === 'string') csrfToken = rotatedToken;
    return response;
  },
  async (error) => {
    const original = error.config as RetryConfig | undefined;
    if (error.response?.status !== 401 || !original || original._retry
      || AUTH_LIFECYCLE.test(original.url || '')) return Promise.reject(error);
    try {
      await refreshSession();
    } catch {
      csrfToken = null;
      const { useAuthStore } = await import('../stores/authStore');
      useAuthStore.getState().clearSession();
      return Promise.reject(error);
    }
    const retry: RetryConfig = { ...original, _retry: true };
    return client(retry);
  }
);

export default client;
