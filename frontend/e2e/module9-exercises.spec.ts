import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE9_BASE = '/module/writing-cleaner-code/lesson/practice-cleaner-code/exercise';

test.describe('Module 9 New Exercise Validation', () => {
  test('squares-list: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE9_BASE}/squares-list`);
    await expect(page.getByRole('heading', { name: 'Squares List' })).toBeVisible();

    await typeInMonaco(page, 'squares = [n ** 2 for n in range(1, 11)]\nprint(squares)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('squares-list: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE9_BASE}/squares-list`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('fix-the-comprehension: correct fix passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE9_BASE}/fix-the-comprehension`);
    await expect(page.getByRole('heading', { name: 'Fix the Comprehension' })).toBeVisible();

    await typeInMonaco(page, 'evens = [n for n in range(10) if n % 2 == 0]\nprint(evens)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('fix-the-comprehension: submitting buggy code shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE9_BASE}/fix-the-comprehension`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });
});
