import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE4_BASE = '/module/loops/lesson/practice-loops/exercise';

test.describe('Module 4 New Exercise Validation', () => {
  test('countdown: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE4_BASE}/countdown`);
    await expect(page.getByRole('heading', { name: 'Countdown' })).toBeVisible();

    await typeInMonaco(page, 'n = 5\n\nwhile n >= 1:\n    print(n)\n    n = n - 1\n\nprint("Go!")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('countdown: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE4_BASE}/countdown`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('break-on-target: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE4_BASE}/break-on-target`);
    await expect(page.getByRole('heading', { name: 'Break on Target' })).toBeVisible();

    await typeInMonaco(
      page,
      'fruits = ["apple", "banana", "cherry", "date"]\n\nfor fruit in fruits:\n    if fruit == "cherry":\n        print("Found it!")\n        break\n    print(fruit)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('break-on-target: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE4_BASE}/break-on-target`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });
});
