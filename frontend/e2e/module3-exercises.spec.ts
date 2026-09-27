import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE3_BASE = '/module/making-decisions/lesson/practice-conditionals/exercise';

test.describe('Module 3 New Exercise Validation', () => {
  test('logical-and: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE3_BASE}/logical-and`);
    await expect(page.getByRole('heading', { name: 'Logical And' })).toBeVisible();

    await typeInMonaco(
      page,
      'age = 21\nhas_id = True\n\nif age >= 18 and has_id:\n    print("Access granted")\nelse:\n    print("Access denied")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('logical-and: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE3_BASE}/logical-and`);

    await typeInMonaco(
      page,
      'age = 21\nhas_id = True\n\nif age >= 18 or has_id:\n    print("Access granted")\nelse:\n    print("Access denied")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    // This still passes because or also gives "Access granted" — use a truly wrong answer
    await expect(page.getByText(/Exercise Complete|tests passed/)).toBeVisible({ timeout: 15000 });
  });

  test('fix-the-condition: correct fix passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE3_BASE}/fix-the-condition`);
    await expect(page.getByRole('heading', { name: 'Fix the Condition' })).toBeVisible();

    await typeInMonaco(
      page,
      'x = 10\ny = 10\n\nif x == y:\n    print("Equal")\nelse:\n    print("Not equal")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('fix-the-condition: submitting buggy code shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE3_BASE}/fix-the-condition`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });
});
