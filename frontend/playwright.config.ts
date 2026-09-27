import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: 'html',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:5187',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: [
    {
      command: 'cd ../backend && uv run --frozen python manage.py runserver 8017 --noreload',
      env: { DJANGO_SETTINGS_MODULE: 'config.settings.e2e', DOTENV_DISABLED: '1' },
      url: 'http://localhost:8017/api/v1/health/',
      reuseExistingServer: false,
      timeout: 15000,
    },
    {
      command: 'npm run dev -- --port 5187 --strictPort',
      env: { PYSTARTER_BACKEND_URL: 'http://127.0.0.1:8017' },
      url: 'http://localhost:5187',
      reuseExistingServer: false,
      timeout: 15000,
    },
  ],
});
