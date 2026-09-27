import { test, expect } from '@playwright/test';
import { registerUser } from './helpers';

test.describe('Hint System', () => {
  test('can reveal hints for an exercise', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/say-hello'
    );

    // Should show hint button with count
    await expect(page.getByText(/Reveal Hint/)).toBeVisible();

    // Reveal first hint
    await page.getByText(/Reveal Hint/).click();

    // Should show hint content (Nudge level - no XP penalty)
    await expect(page.getByText('Nudge')).toBeVisible({ timeout: 5000 });
    await expect(
      page.getByText('function that displays text on screen', { exact: false })
    ).toBeVisible();
  });

  test('hint count updates after revealing', async ({ page }) => {
    await registerUser(page);

    await page.goto(
      '/module/your-first-program/lesson/practice-print/exercise/say-hello'
    );

    // Check initial count shows 0/2
    await expect(page.getByText('0/2')).toBeVisible();

    // Reveal first hint
    await page.getByText(/Reveal Hint/).click();
    await expect(page.getByText('1/2')).toBeVisible({ timeout: 5000 });

    // Reveal second hint
    await page.getByText(/Reveal Hint/).click();
    await expect(page.getByText('Concept')).toBeVisible({ timeout: 5000 });
  });
});
