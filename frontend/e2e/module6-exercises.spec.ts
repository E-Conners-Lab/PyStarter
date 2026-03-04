import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE6_BASE = '/module/lists-and-tuples/lesson/practice-lists/exercise';

test.describe('Module 6 New Exercise Validation', () => {
  test('unpack-the-tuple: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE6_BASE}/unpack-the-tuple`);
    await expect(page.getByRole('heading', { name: 'Unpack the Tuple' })).toBeVisible();

    await typeInMonaco(
      page,
      'person = ("Alice", 25, "Boston")\n\nname, age, city = person\nprint(f"{name} is {age} from {city}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('unpack-the-tuple: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE6_BASE}/unpack-the-tuple`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('sort-and-slice: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE6_BASE}/sort-and-slice`);
    await expect(page.getByRole('heading', { name: 'Sort and Slice' })).toBeVisible();

    await typeInMonaco(
      page,
      'scores = [42, 88, 65, 95, 76, 33]\n\nscores.sort(reverse=True)\nfor s in scores[:3]:\n    print(s)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('sort-and-slice: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE6_BASE}/sort-and-slice`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });
});
