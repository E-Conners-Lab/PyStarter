import { test, expect } from '@playwright/test';

test.describe('Health Check', () => {
  test('GET /api/v1/health/ returns 200 with correct shape', async ({ request }) => {
    const response = await request.get('/api/v1/health/');
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toHaveProperty('status', 'ok');
    expect(body).toHaveProperty('version');
    expect(body).toHaveProperty('database', 'connected');
  });
});
