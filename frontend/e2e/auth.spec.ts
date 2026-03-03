import { test, expect } from '@playwright/test';
import { registerUser } from './helpers';

test.describe('Authentication', () => {
  test('home page loads and shows landing content', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Learn Python from Zero')).toBeVisible();
    await expect(page.getByText('Start Learning')).toBeVisible();
  });

  test('user can register and is redirected to dashboard', async ({ page }) => {
    const { username } = await registerUser(page);

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Your Learning Path')).toBeVisible();
    // Header should show username and 0 XP
    await expect(page.getByText(username)).toBeVisible();
    await expect(page.locator('header').getByText('0 XP')).toBeVisible();
  });

  test('user can log out and log back in', async ({ page }) => {
    const { username, password } = await registerUser(page);

    // Log out
    await page.getByRole('button', { name: 'Logout' }).click();
    await expect(page.getByText('Get Started')).toBeVisible();

    // Log back in
    await page.goto('/login');
    await page.getByLabel('Username').fill(username);
    await page.getByLabel('Password').fill(password);
    await page.getByRole('button', { name: 'Log In' }).click();
    await page.waitForURL('/dashboard');
    await expect(page.getByText(username)).toBeVisible();
  });

  test('unauthenticated user is redirected to login', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });

  test('registration fails with duplicate username', async ({ page }) => {
    const { username } = await registerUser(page);

    // Log out and try to register with same username
    await page.getByRole('button', { name: 'Logout' }).click();
    await page.goto('/register');
    await page.getByLabel('Username').fill(username);
    await page.getByLabel('Email').fill('other@example.com');
    await page.getByLabel('Password').fill('TestPass123!');
    await page.getByRole('button', { name: 'Create Free Account' }).click();

    // Should show error, not redirect
    await expect(page.locator('.text-red-400')).toBeVisible({ timeout: 5000 });
  });
});
