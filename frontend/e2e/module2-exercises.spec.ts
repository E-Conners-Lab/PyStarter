import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE2_BASE = '/module/variables-and-data-types/lesson/practice-variables/exercise';

test.describe('Module 2 Exercise Validation', () => {
  test('create-a-variable: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/create-a-variable`);
    await expect(page.getByRole('heading', { name: 'Create a Variable' })).toBeVisible();

    await typeInMonaco(page, 'message = "Hello, Python!"\nprint(message)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    // Verify XP was awarded (10 XP for this exercise)
    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('math-with-variables: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/math-with-variables`);
    await expect(page.getByRole('heading', { name: 'Math with Variables' })).toBeVisible();

    await typeInMonaco(page, 'width = 10\nheight = 5\nprint(width * height)');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('predict-the-output: selecting correct choice awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/predict-the-output`);
    await expect(page.getByRole('heading', { name: 'Predict the Output' })).toBeVisible();

    // Should show multiple choice options, not a code editor
    await expect(page.getByText('Check Answer')).toBeVisible();

    // Select the correct answer: "8"
    await page.locator('button').filter({ hasText: '8' }).click();
    await page.getByText('Check Answer').click();

    // Should show correct feedback
    await expect(page.getByText('Correct! Great job!')).toBeVisible({ timeout: 5000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('predict-the-output: selecting wrong choice shows error', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/predict-the-output`);

    // Select wrong answer: "5"
    await page.locator('button').filter({ hasText: '5' }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Not quite! Try again.')).toBeVisible({ timeout: 5000 });

    // No XP should be awarded
    const xp = await getHeaderXP(page);
    expect(xp).toBe(0);
  });

  test('introduction-card: correct answer passes and awards 20 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/introduction-card`);
    await expect(page.getByRole('heading', { name: 'Introduction Card' })).toBeVisible();

    await typeInMonaco(
      page,
      'name = "Sam"\nage = 20\ncity = "Austin"\nprint("Name:", name)\nprint("Age:", age)\nprint("City:", city)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(20);
  });

  test('introduction-card: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE2_BASE}/introduction-card`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();

    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('cumulative XP: completing multiple exercises accumulates XP correctly', async ({
    page,
  }) => {
    test.setTimeout(60000);
    await registerUser(page);

    // Exercise 1: create-a-variable (10 XP)
    await page.goto(`${MODULE2_BASE}/create-a-variable`);
    await typeInMonaco(page, 'message = "Hello, Python!"\nprint(message)');
    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });
    await page.waitForTimeout(1000);
    expect(await getHeaderXP(page)).toBe(10);

    // Exercise 2: math-with-variables (15 XP) — cumulative: 25
    await page.goto(`${MODULE2_BASE}/math-with-variables`);
    await typeInMonaco(page, 'width = 10\nheight = 5\nprint(width * height)');
    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });
    await page.waitForTimeout(1000);
    expect(await getHeaderXP(page)).toBe(25);

    // Exercise 3: introduction-card (20 XP) — cumulative: 45
    await page.goto(`${MODULE2_BASE}/introduction-card`);
    await typeInMonaco(
      page,
      'name = "Sam"\nage = 20\ncity = "Austin"\nprint("Name:", name)\nprint("Age:", age)\nprint("City:", city)'
    );
    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });
    await page.waitForTimeout(1000);
    expect(await getHeaderXP(page)).toBe(45);
  });
});
