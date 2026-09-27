import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE5_BASE = '/module/functions/lesson/practice-functions/exercise';

test.describe('Module 5 New Exercise Validation', () => {
  test('default-greeting: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE5_BASE}/default-greeting`);
    await expect(page.getByRole('heading', { name: 'Default Greeting' })).toBeVisible();

    await typeInMonaco(
      page,
      'def greet(name, greeting="Hello"):\n    print(f"{greeting}, {name}!")\n\ngreet("Alice")\ngreet("Bob", "Hey")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('default-greeting: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE5_BASE}/default-greeting`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('fix-the-return: correct fix passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE5_BASE}/fix-the-return`);
    await expect(page.getByRole('heading', { name: 'Fix the Return' })).toBeVisible();

    await typeInMonaco(page, 'def double(n):\n    return n * 2\n\nresult = double(7)\nprint(result)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('fix-the-return: submitting buggy code shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE5_BASE}/fix-the-return`);

    await typeInMonaco(page, 'def double(n):\n    print(n * 2)\n\nresult = double(7)\nprint(result)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });
});
