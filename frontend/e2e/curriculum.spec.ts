import { test, expect } from '@playwright/test';
import { registerUser } from './helpers';

test.describe('Curriculum Navigation', () => {
  test('dashboard shows all modules with first unlocked', async ({ page }) => {
    await registerUser(page);

    await expect(page.getByRole('heading', { name: 'Your Learning Path' })).toBeVisible();
    await expect(page.getByText('Your First Program')).toBeVisible();
    await expect(page.getByText('Variables & Data Types')).toBeVisible();
  });

  test('can navigate into a module and see lessons', async ({ page }) => {
    await registerUser(page);

    await page.getByRole('link', { name: /Your First Program/ }).click();
    await page.waitForURL(/\/module\/your-first-program/);

    await expect(page.getByRole('heading', { name: 'Your First Program' })).toBeVisible();
    await expect(page.getByRole('link', { name: /What is Python/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /The print\(\) Function/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Practice: print\(\)/ })).toBeVisible();
  });

  test('can open a concept lesson and see content', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/what-is-python');
    await expect(page.getByRole('heading', { name: 'Welcome to Python!' })).toBeVisible();
    await expect(page.getByRole('button', { name: /Mark as Complete/ })).toBeVisible();
  });

  test('can mark a concept lesson as complete', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/what-is-python');
    await page.getByRole('button', { name: /Mark as Complete/ }).click();

    // Should redirect back to module
    await page.waitForURL(/\/module\/your-first-program$/);

    // Go back — should show completed
    await page.goto('/module/your-first-program/lesson/what-is-python');
    await expect(page.getByText('Lesson completed')).toBeVisible();
  });

  test('interactive lesson has a code sandbox', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/the-print-function');
    // The sandbox label in the editor chrome
    await expect(page.locator('text=🧪 Try it yourself')).toBeVisible();
    await expect(page.getByRole('button', { name: /Run/ })).toBeVisible();
  });

  test('exercise lesson shows exercise list', async ({ page }) => {
    await registerUser(page);

    await page.goto('/module/your-first-program/lesson/practice-print');
    await expect(page.getByRole('link', { name: /Say Hello/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Print Your Name/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Fix the Bug/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Math Printer/ })).toBeVisible();
  });
});
