import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

test.describe('Exercise Submission & XP', () => {
  test('can view an exercise with instructions and editor', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/say-hello'
    );
    await expect(page.getByRole('heading', { name: 'Say Hello' })).toBeVisible();
    await expect(page.locator('text=FILL BLANK')).toBeVisible();
    await expect(page.getByRole('button', { name: /Run/ })).toBeVisible();
    await expect(page.getByRole('button', { name: /Submit/ })).toBeVisible();
  });

  test('submitting correct code awards XP and updates header', async ({ page }) => {
    await registerUser(page);

    const startingXP = await getHeaderXP(page);
    expect(startingXP).toBe(0);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/say-hello'
    );

    await typeInMonaco(page, 'print("Hello, World!")');

    await page.getByRole('button', { name: /Submit/ }).click();

    // Wait for success result
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    // XP in header should have updated
    await page.waitForTimeout(2000);
    const updatedXP = await getHeaderXP(page);
    expect(updatedXP).toBeGreaterThan(0);
  });

  test('submitting wrong code shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/print-your-name'
    );

    await typeInMonaco(page, 'print("wrong answer")');

    await page.getByRole('button', { name: /Submit/ }).click();

    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('running code shows test results without awarding XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/math-printer'
    );

    await typeInMonaco(page, 'print(7 * 8)');

    await page.getByRole('button', { name: '▶ Run' }).click();

    await expect(page.getByText('Tests Passed')).toBeVisible({ timeout: 10000 });

    const xp = await getHeaderXP(page);
    expect(xp).toBe(0);
  });

  test('XP persists after page reload', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/say-hello'
    );
    await typeInMonaco(page, 'print("Hello, World!")');
    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(2000);
    const xpBefore = await getHeaderXP(page);
    expect(xpBefore).toBeGreaterThan(0);

    // Reload and check XP persists
    await page.reload();
    await page.waitForSelector('header', { timeout: 10000 });
    await page.waitForTimeout(2000);

    const xpAfter = await getHeaderXP(page);
    expect(xpAfter).toBe(xpBefore);
  });
});
