import { test, expect } from '@playwright/test';

test.describe('404 Page', () => {
  test('renders 404 on unknown route', async ({ page }) => {
    await page.goto('/definitely-not-a-page');
    await expect(page.getByText('404')).toBeVisible();
    await expect(page.getByText('Page not found')).toBeVisible();
  });

  test('"Go Home" link navigates to /', async ({ page }) => {
    await page.goto('/definitely-not-a-page');
    await page.getByText('Go Home').click();
    await expect(page).toHaveURL('/');
  });
});
