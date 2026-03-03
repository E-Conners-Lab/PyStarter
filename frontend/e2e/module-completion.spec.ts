import { test, expect } from '@playwright/test';
import { registerUser, typeInMonaco } from './helpers';

test.describe('Module Completion Flow', () => {
  test('completing all module content shows continue-to-next-module buttons', async ({
    page,
  }) => {
    test.setTimeout(120000);

    await registerUser(page);

    // ── Complete the two concept/interactive lessons ──

    await page.goto('/module/your-first-program/lesson/what-is-python');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();
    await page.waitForURL(/\/module\/your-first-program$/);

    await page.goto('/module/your-first-program/lesson/the-print-function');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();
    await page.waitForURL(/\/module\/your-first-program$/);

    // ── Complete first 3 exercises ──

    const exercises = [
      { slug: 'say-hello', code: 'print("Hello, World!")' },
      { slug: 'print-your-name', code: 'print("My name is Python")\nprint("I love coding!")' },
      { slug: 'fix-the-bug', code: 'print("Python is fun!")' },
    ];

    for (const ex of exercises) {
      await page.goto(
        `/module/your-first-program/lesson/practice-print/exercise/${ex.slug}`
      );
      await typeInMonaco(page, ex.code);
      await page.getByRole('button', { name: /Submit/ }).click();
      await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

      // After exercise (not the last one), should see "Next Exercise" button
      await expect(page.getByRole('link', { name: /Next Exercise/ })).toBeVisible();
    }

    // ── Complete the last exercise (math-printer) ──

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/math-printer'
    );
    await typeInMonaco(page, 'print(7 * 8)');
    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    // Wait for module/lesson queries to refetch after invalidation
    await page.waitForTimeout(2000);

    // After last exercise, should show "Continue to next module" on the exercise page
    await expect(
      page.getByText('Module complete! Nice work!')
    ).toBeVisible({ timeout: 5000 });
    await expect(
      page.getByRole('link', { name: /Continue to Variables & Data Types/ })
    ).toBeVisible();

    // ── Navigate to lesson page — should also show continue banner ──

    await page.goto('/module/your-first-program/lesson/practice-print');
    await expect(page.getByText('All exercises complete!')).toBeVisible();
    await expect(
      page.getByRole('link', { name: /Continue to Variables & Data Types/ })
    ).toBeVisible();

    // ── Navigate to module page — should show module complete banner ──

    await page.goto('/module/your-first-program');
    await expect(page.getByText('Module Complete!')).toBeVisible();
    await expect(
      page.getByRole('link', { name: /Continue to Variables & Data Types/ })
    ).toBeVisible();

    // ── Click the button and land on Module 2 ──

    await page.getByRole('link', { name: /Continue to Variables & Data Types/ }).click();
    await page.waitForURL(/\/module\/variables-and-data-types/);
    await expect(
      page.getByRole('heading', { name: 'Variables & Data Types' })
    ).toBeVisible();
  });
});
