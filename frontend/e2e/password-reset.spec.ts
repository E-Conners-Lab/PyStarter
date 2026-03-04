import { test, expect } from '@playwright/test';

test.describe('Password Reset', () => {
  test('forgot password page loads from login link', async ({ page }) => {
    await page.goto('/login');
    await page.getByText('Forgot your password?').click();
    await expect(page).toHaveURL('/forgot-password');
    await expect(page.getByText('Reset Password')).toBeVisible();
  });

  test('forgot password form submits and shows success', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByRole('button', { name: 'Send Reset Link' }).click();
    await expect(page.getByText('reset link has been sent')).toBeVisible({ timeout: 5000 });
  });

  test('reset password page loads with uid/token params', async ({ page }) => {
    await page.goto('/reset-password/abc123/def456');
    await expect(page.getByText('Set New Password')).toBeVisible();
    await expect(page.getByLabel('New Password')).toBeVisible();
    await expect(page.getByLabel('Confirm Password')).toBeVisible();
  });
});
