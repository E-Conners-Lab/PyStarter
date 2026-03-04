import { test, expect } from '@playwright/test';
import { registerUser, typeInMonaco } from './helpers';

test.describe('Module Progression', () => {
  test('profile page shows progress stats', async ({ page }) => {
    await registerUser(page);

    await page.goto('/profile');
    await expect(page.getByRole('heading', { name: 'Your Profile' })).toBeVisible();
    await expect(page.getByText('White Belt')).toBeVisible();
    await expect(page.getByText('Modules Completed')).toBeVisible();
    await expect(page.getByText('Exercises Completed')).toBeVisible();
  });

  test('completing all module 1 content unlocks module 2', async ({ page }) => {
    test.setTimeout(120000); // This is a long test

    await registerUser(page);

    // Check that module 2 is locked (not a clickable link)
    await page.goto('/dashboard');
    await expect(page.locator('a[href="/module/variables-and-data-types"]')).toHaveCount(0);

    // Complete concept lesson
    await page.goto('/module/your-first-program/lesson/what-is-python');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();
    await page.waitForURL(/\/module\/your-first-program$/);

    // Complete interactive lesson
    await page.goto('/module/your-first-program/lesson/the-print-function');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();
    await page.waitForURL(/\/module\/your-first-program$/);

    // Complete the Try It Yourself lesson
    await page.goto('/module/your-first-program/lesson/try-it-yourself-print');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();
    await page.waitForURL(/\/module\/your-first-program$/);

    // Complete all 4 exercises
    const exercises = [
      { slug: 'say-hello', code: 'print("Hello, World!")' },
      { slug: 'print-your-name', code: 'print("My name is Python")\nprint("I love coding!")' },
      { slug: 'fix-the-bug', code: 'print("Python is fun!")' },
      { slug: 'math-printer', code: 'print(7 * 8)' },
    ];

    for (const ex of exercises) {
      await page.goto(
        `/module/your-first-program/lesson/practice-print/exercise/${ex.slug}`
      );
      await typeInMonaco(page, ex.code);
      await page.getByRole('button', { name: /Submit/ }).click();
      await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });
    }

    // Go back to dashboard — Module 2 should now be unlocked
    await page.goto('/dashboard');
    await page.waitForTimeout(1000);
    await expect(page.locator('a[href="/module/variables-and-data-types"]')).toBeVisible({
      timeout: 5000,
    });
  });
});
