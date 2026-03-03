import { test, expect } from '@playwright/test';
import { registerUser, typeInMonaco } from './helpers';

test.describe('Interactive Sandbox', () => {
  test('sandbox executes code and shows output', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/the-print-function');

    await expect(page.locator('text=🧪 Try it yourself')).toBeVisible();
    await page.waitForSelector('.monaco-editor', { timeout: 10000 });

    // Run the pre-loaded code
    await page.getByRole('button', { name: /Run/ }).click();

    // Should show output containing Hello, World!
    await expect(page.locator('pre').filter({ hasText: 'Hello, World!' })).toBeVisible({
      timeout: 10000,
    });
  });

  test('sandbox shows errors for bad code', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/the-print-function');

    await typeInMonaco(page, 'print(hello)');

    await page.getByRole('button', { name: /Run/ }).click();

    // Should show error output
    await page.waitForTimeout(2000);
    const outputArea = page.locator('pre').last();
    await expect(outputArea).toBeVisible({ timeout: 10000 });
    const text = await outputArea.textContent();
    expect(text).toMatch(/Name Error|NameError|name 'hello' is not defined/);
  });
});
