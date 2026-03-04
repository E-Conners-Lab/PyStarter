import { test, expect } from '@playwright/test';
import { registerUser, getHeaderXP, typeInMonaco } from './helpers';

const MODULE12_BASE = '/module/user-input-and-while-loops/lesson/practice-user-input/exercise';

test.describe('Module 12 Exercise Validation', () => {
  test('greet-the-user: correct answer passes and awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/greet-the-user`);
    await expect(page.getByRole('heading', { name: 'Greet the User' })).toBeVisible();

    await typeInMonaco(page, 'name = input()\nprint(f"Hello, {name}!")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('greet-the-user: wrong answer shows failure', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/greet-the-user`);

    await typeInMonaco(page, 'print("wrong")');

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/tests passed/)).toBeVisible({ timeout: 10000 });
  });

  test('sum-until-quit: correct answer passes and awards 15 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/sum-until-quit`);
    await expect(page.getByRole('heading', { name: 'Sum Until Quit' })).toBeVisible();

    await typeInMonaco(
      page,
      'total = 0\nwhile True:\n    line = input()\n    if line == "done":\n        break\n    total += int(line)\nprint(total)'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(15);
  });

  test('predict-the-while-loop: correct choice awards 10 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/predict-the-while-loop`);
    await expect(page.getByRole('heading', { name: 'Predict the Loop' })).toBeVisible();

    await page.getByRole('button', { name: '7 4 1', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Correct! Great job!')).toBeVisible({ timeout: 5000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(10);
  });

  test('predict-the-while-loop: wrong choice shows error', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/predict-the-while-loop`);

    await page.getByRole('button', { name: '7 4', exact: true }).click();
    await page.getByText('Check Answer').click();

    await expect(page.getByText('Not quite! Try again.')).toBeVisible({ timeout: 5000 });
  });

  test('number-checker: correct answer passes and awards 20 XP', async ({ page }) => {
    await registerUser(page);

    await page.goto(`${MODULE12_BASE}/number-checker`);
    await expect(page.getByRole('heading', { name: 'Number Checker' })).toBeVisible();

    await typeInMonaco(
      page,
      'pos = 0\nneg = 0\nzero = 0\nwhile True:\n    line = input()\n    if line == "stop":\n        break\n    num = int(line)\n    if num > 0:\n        print("positive")\n        pos += 1\n    elif num < 0:\n        print("negative")\n        neg += 1\n    else:\n        print("zero")\n        zero += 1\nprint(f"Positive: {pos} Negative: {neg} Zero: {zero}")'
    );

    await page.getByRole('button', { name: /Submit/ }).click();
    await expect(page.getByText(/Exercise Complete/)).toBeVisible({ timeout: 15000 });

    await page.waitForTimeout(1000);
    const xp = await getHeaderXP(page);
    expect(xp).toBe(20);
  });
});
